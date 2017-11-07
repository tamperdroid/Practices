#
# List script 
	#	coffee run.coffee davidlawrence-au list 0
# SKU History script 
	# 	coffee run.coffee davidlawrence-au sku-history
# Workers	
	#coffee run.coffee davidlawrence-au workers
	
try
	# shared = require('./shared')
	shared = require('/opt/goldrush-worker/shared')
	retailerCode = process.argv[2].toLowerCase()
	retailer_group_name = process.argv[3]
	consumer_machine_ip = process.argv[5].toString()
	if(consumer_machine_ip.match(/retailer_consumer/i))
		consumer_machine_ip ='127.0.0.1'
	shared.common_redisConfig['IP'] = consumer_machine_ip
	console.log(shared.common_redisConfig['IP'])
	# shared.mysqlConfig['database'] =  "scraper_"+retailerCode.replace("-","")
	# shared.mysqlConfig['database'] ="davidlawrence_ginger"
	# shared.mysqlConfig['database'] =  "scraper_davidlawrence"
	if retailerCode != "setup-retailer" and retailerCode != "market-facet-entries"
		# retailerScript = require('./'+retailerCode)
		retailerScript = require('/opt/goldrush-worker/robots/'+retailerCode)
catch e
	console.error e.message, if e.code == 'MODULE_NOT_FOUND' then 'please install it (npm install module_name)' else ''
	process.exit e.code

dateReg = /^\d{4}([./-])\d{2}\1\d{2}$/



#----------------------------------------------------------------------------------------------------------------------------------
listWorkers = ->
	deferred = shared.q.defer()
	retailerScript.getFirstLevelMenuUrls(shared.retailer)
	.then(retailerScript.getSecondLevelMenuUrls)
	.then(retailerScript.getDeepUrls)
	.then(retailerScript.getFacetsUrls)
	.then(retailerScript.addProductsToRedis)
	.then(retailerScript.getProductsFromRedis.bind(retailerCode:shared.retailer.retailer_code))
	.fail((err) ->
		shared.errorLogger "*Error, " , err
	).end
	deferred.promise

#----------------------------------------------------------------------------------------------------------------------------------
# Consumer handles the detail info collection based on the msg rate.
skuHistory = ->
	deferred = shared.q.defer()
	shared.producer()
	.fail((err) ->
		shared.errorLogger "*Error, " , err
	).end

	deferred.promise
	
worker = ->
	deferred = shared.q.defer()
	shared.consumer(shared.retailer.retailer_code,retailerScript)
	.fail((err) ->
		shared.errorLogger "*Error, " , err
	).end

	deferred.promise
localToCommanRedis = ->
	deferred = shared.q.defer()
	shared.q(shared.retailer.retailer_code)
	.then(retailerScript.getProductsFromRedis.bind(retailerCode:shared.retailer.retailer_code))
	.fail((err) ->
		shared.errorLogger "*Error, " , err
	).end

	deferred.promise
#----------------------------------------------------------------------------------------------------------------------------------
#main routine
if process.argv.length >= 4
	if process.argv.length == 5 and process.argv[4].match(dateReg) 
		shared.reportingDate = process.argv[4]
	if process.argv[4] == 'sku-history'
		shared.isRedisServeraLive()
		.then(shared.comman_isRedisServeraLive())
		.then(shared.getRetailerData.bind(retailerCode:retailerCode))
		.then(skuHistory)
		.fail((err) ->
			shared.detailLogger "*" , err
		).end

	else if process.argv[4] == 'list'
		shared.isRedisServeraLive()
		.then(shared.comman_isRedisServeraLive())		
		.then(shared.isImageDirectoryExist.bind(retailerCode:retailerCode))
		.then(shared.getRetailerData.bind(retailerCode:retailerCode,0))
		.then(listWorkers)
		.then(shared.listLogger)
		.then(console.log)
		.fail((err) ->
			shared.listLogger "*" , err
		).end
		
	else if process.argv[4] == 'workers'
		shared.isRedisServeraLive()
		.then(shared.comman_isRedisServeraLive())
		.then(shared.getRetailerData.bind(retailerCode:retailerCode))
		.then(shared.CacheBrandLogic())
		.then(worker)
		.fail((err) ->
			shared.detailLogger "*" , err
		).end
	else if process.argv[4] == 'ltoc'
		shared.isRedisServeraLive()
		.then(shared.comman_isRedisServeraLive())
		.then(shared.getRetailerData.bind(retailerCode:retailerCode))
		.then(localToCommanRedis)
		.fail((err) ->
			shared.detailLogger "*" , err
		).end
	else if process.argv[4] == 'cacheterms'
		shared.isRedisServeraLive()
		.then(shared.CacheTerms())
		.fail((err) ->
			shared.detailLogger "*" , err
		).end
	else if process.argv[4] == 'cacheskus'
		shared.isRedisServeraLive()
		.then(shared.CacheSkus())
		.fail((err) ->
			shared.detailLogger "*" , err
		).end
	else if process.argv[4] == 'cacheproduct'
		shared.isRedisServeraLive()
		.then(shared.CacheProduct())
		.fail((err) ->
			shared.detailLogger "*" , err
		).end
	# addRetailer = (retailerName, retailerNormalizedName, retailerCode,retailerWebsiteURL,locale,countryCode,retailergroupName,hitspersecond,pricegroupname,proxy,update)
		# parameters
			# 1	retailerName 					# example : david lawrence au
			# 2	retailerNormalizedName			#			david lawrence
			# 3	retailerCode 					#			davidlawrence-au
			# 4	retailerWebsiteURL 				#			http://www.davidlawrence.com.au
			# 5	locale 							#			en_AU
			# 6 countryCode 					#			AU
			# 7 retailergroupName				#			davidlawrence
			# 8 hitspersecond					#			2
			# 9 pricegroupname					#			premium
			# 10 proxy							#			http://frawspcpx.cloud.trendinglines.co.uk:3130

	else if process.argv[2] == 'setup-retailer' and process.argv.length == 14
		shared.addRetailer(process.argv[3], process.argv[4], process.argv[5], process.argv[6],process.argv[7],process.argv[8],process.argv[9],process.argv[10],process.argv[11],process.argv[12],process.argv[13])
		.then(console.log)
		.fail((err) ->
			console.log "*" , err
		).end

	# add / edit / delete as action
	# facets to work on facets, markets to work on markets
	# market or facet name as third parameter 
	# retailer code
	


	else if process.argv[2].toLowerCase() == 'market-facet-entries' and ( process.argv[4].toLowerCase() == "facets" or process.argv[4].toLowerCase() == "markets")
		action = process.argv[3]
		table = process.argv[4]
		name = process.argv[5]
		retailerCode = process.argv[6]
		enabled = process.argv[7]

		shared.marketFacetEntries(action, table + "_scraper", name, retailerCode,enabled)
		.then(console.log)
		.fail((err) ->
			console.log "*" , err
		).end

else
	console.log "Command help: coffee run.coffee retailer_code action optional:(report date in YYYY-MM-DD)"
	console.log "\tavailable actions are (list, sku-history, add-retailer, market-facet-entries)"
	console.log process.argv[2]

