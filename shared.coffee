#configuration
#____________________________________________________________________________________________________________________


#require config file
config = require('/opt/goldrush-worker/config')
#config = require('./config')


#assign required npm modules from config to a variable modules and export it
modules = config.modules
exports = module.exports = modules

#list logs


exports.listLogger = config.listLogger.list

#logs in detail collection
exports.detailLogger = config.detailLogger.detail

#logs in dberror collection
exports.dberrLogger = config.dberrLogger.dberr

exports.collectionCompletedLogger= config.collectionCompletedLogger.collectionCompleted

exports.errorLogger= config.errorLogger.error

exports.imageLogger = config.imageLogger.image



pingLogger = config.redisConfig

#Redis server configuration
exports.redisConfig = config.redisConfig

exports.common_redisConfig = config.common_redisConfig

exports.translation_redisConfig = 	config.translation_redisConfig

exports.server_ip_client_redisConfig = config.server_ip_client_redisConfig

exports.luminatiSuperProxy=config.luminatiSuperProxy

#MYSQL server configuration
mysqlConfig = config.mysqlConfig
exports.mysqlConfig = mysqlConfig

#MYSQL server configuration for qa_db
exports.mysqlConfig_qa_db = config.mysqlConfig_qa_db

#MYSQL server configuration for Management_Console_Config
exports.Management_Console_Config = config.Management_Console_Config

exports.aws_keys = config.aws_keys
  
# NFS path for downloading images.
imagePath= config.imagePath

#Maximum number of trials before download URL give up.
maxTrials = config.maxTrials 		#Max trial for http get before it give up.

#Pause after each download.
timeout = config.timeout		#Interval between each http get.

#Cache INSTOCK taxonomy tree.
taxonomiesCache = {}

#Stemmed version of Cache INSTOCK taxonomy tree.
stemmedTaxonomiesCache = {}

#Stored all retailer ips
exports.retailer_group_data=[]

#Retailer details
	# { ... 
	# retailer_id: ,
	# retailer_locale_id: ,
	# retailer_website_url: ',
	# retailer_code: ,
	# country_id: 
	# ....}
exports['retailer'] = {}

#Separator
exports['splitter'] = "¶"
exports['list_control_time']
#Authentication JSON 
exports.auth =
	method: 'GET'
	json : true
	timeout: 40000
	headers: 
		Content_Type : 'application/x-www-form-urlencoded'
todayDate = new Date()
#Today's date in UTC format
exports['reportingDate'] = new Date(new Date().toUTCString()).toISOString().slice(0, 19).replace("T", " ")
todayDate.setDate (todayDate.getDate() - 1)

#Yesterday's date in UTC format
exports['reportingYesterdayDate'] = new Date(todayDate.toUTCString()).toISOString().slice(0, 19).replace("T", " ")
exports.Super_proxy=''
#____________________________________________________________________________________________________________________
## Check if NodeJS dependencies modules are installed.
## If not stop the script.
#____________________________________________________________________________________________________________________

#npm modules which are used locally

crypto = modules.crypto
fs = modules.fs
mkdirp = modules.mkdirp
md5 = modules.md5
# A library to connect to mysql server
mysql = modules.mysql
_ = modules._

user_agent=config.user_agent
natural = modules.natural
Sdl_Key=config.Sdl_Key
country=config.country
exports.country_code=""
exports.country_value=""
exports.jobs = exports.kue.createQueue()

proxy_detail=""
imageHash = new exports.HashMap()

#Initiate redis client
exports.client = exports.redis.createClient(exports.redisConfig.port, exports.redisConfig.IP)
exports.client.setMaxListeners(0)
# #Initiate common_redis client



# Initiate translation_redis client
exports.translation_client = exports.redis.createClient(exports.translation_redisConfig.port, exports.translation_redisConfig.IP)
exports.translation_client.setMaxListeners(0)

#Initiate translation_redis client
exports.server_ip_client = exports.redis.createClient(exports.server_ip_client_redisConfig.port, exports.server_ip_client_redisConfig.IP)
exports.server_ip_client.setMaxListeners(0)


#____________________________________________________________________________________________________________________
#	@desc check if redis server is alive 
#	@param none
#	@return true if redis is alive, otherwise it stop the application.
exports.isRedisServeraLive = ->
	console.log "Checking redis..."
	#Creating a promise
	deferred = exports.q.defer()
	# #Initiate redis client
	# client = exports.redis.createClient(exports.redisConfig.port, exports.redisConfig.IP)
	exports.client.on 'error', (err) ->
		console.log 'ERROR => Cannot connect to Redis server: URL => ' + exports.redisConfig.IP + '; Port => ' + exports.redisConfig.port
		exports.errorLogger 'ERROR => Cannot connect to Redis server: URL => ' + exports.redisConfig.IP + '; Port => ' + exports.redisConfig.port
		deferred.resolve false		
		#Exit if redis server is offline or not installed.
		process.exit 0
	#If redis server is alive return true.
	exports.client.on 'ready', (err) ->
		console.log "\t" + " ... ok"
		exports.client.unsubscribe()
		deferred.resolve true
		
		return
	return deferred.promise

#	@desc check if common redis server is alive 
#	@param none
#	@return true if common redis is alive, otherwise it stop the application.	
exports.comman_isRedisServeraLive = () ->
	console.log "Checking redis... in comman_isRedisServeraLive"
	deferred = exports.q.defer()
	exports.common_client = exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
	exports.common_client.setMaxListeners(0)
	exports.common_client.on 'error', (err) ->
		console.log err
		console.log 'ERROR => Cannot connect to Redis server: URL => ' + exports.common_redisConfig.IP + '; Port => ' + exports.common_redisConfig.port
		exports.errorLogger 'ERROR => Cannot connect to Redis server: URL => ' + exports.common_redisConfig.IP + '; Port => ' + exports.common_redisConfig.port
		deferred.resolve false		
		#Exit if redis server is offline or not installed.
		process.exit 0
	#If redis server is alive return true.
	exports.common_client.on 'ready', (err) ->
		console.log "\t" + " ... ok"
		# exports.common_client.unsubscribe()
		deferred.resolve true
		
		return
	return deferred.promise
#____________________________________________________________________________________________________________________
# /** 
#	@desc this function will check the existence of retailer folder in NFS repository,if not available It will create a new folder for downloading images in NFS repository.  
#	@param retailerCode
#	@return return null
#  */
exports.isImageDirectoryExist = () ->
	#Creating a promise
	deferred = exports.q.defer()
	retailerCode=@retailerCode
	console.log "Checking ImageDirectory..."
	letters=['A','B','C','D','E','F']
	numbers=[0..9]
	list=numbers.concat(letters)
	for firstlevel in list
		for secondlevel in list
			for thridlevel in list
				path="#{imagePath}/#{retailerCode}/#{firstlevel}/#{secondlevel}/#{thridlevel}"
				stats = fs.existsSync(path)
				if(stats == false)
					mkdirp path, (err) ->
						if(err)
							console.log(err)
							process.exit 0
	console.log "\t" + " ... ok"
	deferred.resolve true		
#____________________________________________________________________________________________________________________
# /** 
#	@desc Initiate mysql connection
#	@param none
#	@return return connection object
#  */
exports.connectToMysql = ->
	#Creating a promise
	deferred = exports.q.defer()
	#Initiate mysql connection store it into mysqlConnection
	mysqlConnection = mysql.createConnection(mysqlConfig)
	mysqlConnection.connect (err) ->
		#If mysql server is down, throw an error
		if err
			exports.dberrLogger '-error when connecting to db:', err.code
			deferred.reject 'error when connecting to db:', err.code
		#If successful return the connection.
		else
			deferred.resolve mysqlConnection
		return
	mysqlConnection.on 'error', (err) ->
		exports.dberrLogger 'error when connecting to db:', err.code
		deferred.reject 'error when connecting to db:', err.code
		return
	deferred.promise


#_______________________________________________________________________________
#	@desc return retailer url,code,country,currency
#	@param Binding param @retailerCode
#	@return return object contains retailer data, Cache it into retailer Object
			# {retailer_id: ,
			# retailer_locale_id: ,
			# retailer_website_url: ,
			# retailer_code: ,
			# country_id: , ... }
# # exports.getRetailerData = () ->
	# # #Create a promise
	# # deferred = exports.q.defer()
	# # retailerCode = @retailerCode
	# # #Connect to mysql 
	# # exports.connectToMysql()
	# # .then (mysqlConnection) ->

		# # sql = " SELECT R.id as retailer_id, R.locale_id as retailer_locale_id, R.website_url as retailer_website_url,R.scraper_url as retailer_scraper_url,R.list_control_time as retailer_list_control_time,R.code as retailer_code,R.user_agent as agent,PS.IP as proxy_detail,RG.name as retailer_group_name,RG.hits_per_second as hits_per_second" \
		# # + " FROM retailers R " \
		# # + " LEFT JOIN retailer_groups RG ON R.group_id = RG.id  " \
		# # + " LEFT JOIN proxy_servers_retailer_groups PSRG ON R.group_id = PSRG.retailer_group_id " \
		# # + " LEFT JOIN proxy_servers PS ON PSRG.proxy_server_id = PS.id " \
		# # + " WHERE R.code = " + mysqlConnection.escape(retailerCode)
		# # mysqlConnection.query sql , (err, rows, fields) ->
			# # console.log(err)
			# # #If the retailer exist in the database
			# # if !err and rows.length > 0
				# # #Close mysql connection
				# # # mysqlConnection.end()

				# # #Cache exports.retailer with retailer details 
				# # exports.retailer = rows[0]
				# # exports.retailer.retailer_list_control_time=exports.retailer.retailer_list_control_time*60000
				# # exports.country_code=exports.retailer.retailer_code
				# # exports.country_code=exports.country_code.match(/\-([^>]*?)$/i)
				# # exports.country_code=	exports.country_code[1]
				# # exports.country_code=exports.country_code.toUpperCase()
				# # exports.auth['proxy']=exports.retailer.proxy_detail
				# # exports.auth['headers']['User-Agent']=user_agent[exports.retailer.agent.toLowerCase()]
				
				# # deferred.resolve exports.retailer
				
			# # else
				# # mysqlConnection.end()
				# # deferred.reject err
	# # return deferred.promise
exports.getRetailerData = () ->
	#Create a promise
	deferred = exports.q.defer()
	retailerCode = @retailerCode
	category="CATEGORY"
	facet="FACET"
	#Connect to mysql 
	exports.connectToMysql()
	.then (mysqlConnection) ->

		sql = " SELECT R.id as retailer_id, R.locale_id as retailer_locale_id, R.website_url as retailer_website_url,R.scraper_url as retailer_scraper_url,R.list_control_time as retailer_list_control_time,R.code as retailer_code,R.user_agent as agent,PS.IP as proxy_detail,RG.name as retailer_group_name,RG.hits_per_second as hits_per_second, " \
		+ " (select group_concat(name  SEPARATOR '" + exports.splitter + "') from scraper_options SO where SO.retailer_id = R.id AND SO.enabled = 1 AND SO.option_type="+mysqlConnection.escape(category)+") as markets_to_scrape, " \
		+ " (select group_concat(name  SEPARATOR '>') from scraper_options SO where SO.retailer_id = R.id AND SO.enabled = 0 AND SO.option_type="+mysqlConnection.escape(category)+") as markets_to_skip, " \
		+ " (select group_concat(name  SEPARATOR '>') from scraper_options SO where SO.retailer_id = R.id AND SO.enabled = 0 AND SO.option_type="+mysqlConnection.escape(facet)+") as facets_to_skip, " \
		+ " (select group_concat(name  SEPARATOR '" + exports.splitter + "') from scraper_options SO where SO.retailer_id = R.id AND SO.enabled = 1 AND SO.option_type="+mysqlConnection.escape(facet)+") as facets_to_scrape " \
		+ " FROM retailers R " \
		+ " LEFT JOIN retailer_groups RG ON R.group_id = RG.id  " \
		+ " LEFT JOIN proxy_servers_retailers PSRG ON R.group_id = PSRG.retailer_id " \
		+ " LEFT JOIN proxy_servers PS ON PSRG.proxy_server_id = PS.id " \
		+ " WHERE R.code = " + mysqlConnection.escape(retailerCode)

		mysqlConnection.query sql , (err, rows, fields) ->
			#If the retailer exist in the database
			if !err and rows.length > 0
				#Close mysql connection
				# mysqlConnection.end()

				#Cache exports.retailer with retailer details 
				exports.retailer = rows[0]
				exports.retailer.retailer_list_control_time=exports.retailer.retailer_list_control_time*60000
				exports.country_code=exports.retailer.retailer_code
				exports.country_code=exports.country_code.match(/\-([^>]*?)$/i)
				exports.country_code=	exports.country_code[1]
				exports.country_code=exports.country_code.toUpperCase()
				exports.country_value=country[exports.country_code]
				exports.auth['proxy']=exports.retailer.proxy_detail
				exports.auth['headers']['User-Agent']=user_agent[exports.retailer.agent.toLowerCase()]
				
				
				# Condition to check if the markets to skip are not null
				if(exports.retailer.markets_to_skip)
					exports.retailer.markets_to_skip=(exports.retailer.markets_to_skip).replace(/amp\;/ig,'')
					exports.retailer.markets_to_skip = exports.retailer.markets_to_skip.split('>')
				# Condition to check if the facets to scrape are not null
				if(exports.retailer.facets_to_scrape)
					exports.retailer.facets_to_scrape=(exports.retailer.facets_to_scrape).replace(/amp\;/ig,'')
					exports.retailer.facets_to_scrape = exports.retailer.facets_to_scrape.split(exports.splitter)
				# Condition to check if the markets to scrape are not null
				if(exports.retailer.markets_to_scrape)
					exports.retailer.markets_to_scrape=(exports.retailer.markets_to_scrape).replace(/amp\;/ig,'')
					exports.retailer.markets_to_scrape = exports.retailer.markets_to_scrape.split(exports.splitter)
				# Condition to check if the facet to skip are not null
				if(exports.retailer.facets_to_skip)
					exports.retailer.facets_to_skip=(exports.retailer.facets_to_skip).replace(/amp\;/ig,'')
					exports.retailer.facets_to_skip = exports.retailer.facets_to_skip.split('>')
				
				old_urls_qurey = 'select distinct product_url from products where last_scrape_utc between subdate(curdate(), interval 7 day) and curdate()'
				# console.log "old_urls_qurey"+old_urls_qurey
				exports.retailer.old_urls_list = []
				exports.retailer.old_urls_count = 0
				mysqlConnection.query old_urls_qurey , (err1, rows1, fields1) ->
					#If the retailer exist in the database
					#Close mysql connection
					mysqlConnection.end()
					if err1
						mysqlConnection.end()
						deferred.reject err1
					else if rows1.length > 0
						exports.retailer.old_urls_count = Object.keys(rows1).length
						rows1.forEach (url) ->
							exports.retailer.old_urls_list.push url.product_url
						deferred.resolve exports.retailer
					else
						deferred.resolve exports.retailer
						
			else
				mysqlConnection.end()
				deferred.reject err
	return deferred.promise
	

exports.get_7_days_urls = (retailer) ->
	#Create a promise
	deferred = exports.q.defer()
	setTimeout (->
		old_urls_qurey = 'select distinct product_url from products where last_scrape_utc between subdate(curdate(), interval 7 day) and curdate()'
		# console.log "old_urls_qurey"+old_urls_qurey
		exports.retailer.old_urls_list = []
		exports.retailer.old_urls_count = 0
		exports.connectToMysql()
		.then (mysqlConnection) ->
			mysqlConnection.query old_urls_qurey , (err1, rows1, fields1) ->
				#If the retailer exist in the database
				#Close mysql connection
				mysqlConnection.end()
				if err1
					mysqlConnection.end()
					deferred.reject err1
				else if rows1.length > 0
					exports.retailer.old_urls_count = Object.keys(rows1).length
					rows1.forEach (url) ->
						(exports.retailer.old_urls_list).push url.product_url
					deferred.resolve exports.retailer
				else
					deferred.resolve exports.retailer
	), 2000						
	deferred.promise
	
exports.market_facet_Collection = (retailer) ->
	#Create a promise
	deferred = exports.q.defer()
	markets=["markets_to_scrape","markets_to_skip","facets_to_scrape","facets_to_skip"]
	index=0
	exports.connectToMysql()
	.then (mysqlConnection) ->
	setTimeout (->
		market_facet = (market, doneCallback) ->
			setTimeout (->
				console.log(market)
				exports.retailer[market]=[]
				category="CATEGORY"
				enabled=1
				if(market.match(/facets/i))
					category="FACET"
				if(market.match(/skip/i))	
					enabled=0
				console.log(category)	
				console.log(enabled)	
				exports.connectToMysql()
				.then (mysqlConnection) ->
					market_query = 'select name from scraper_options where retailer_id = '+mysqlConnection.escape(exports.retailer['retailer_id'])+' AND enabled ='+mysqlConnection.escape(enabled)+' AND option_type='+mysqlConnection.escape(category)
					console.log(market_query)
					mysqlConnection.query market_query , (err1, rows1, fields1) ->
						#If the retailer exist in the database
						#Close mysql connection
						mysqlConnection.end()
						if err1
							mysqlConnection.end()
							deferred.reject err1
						else if rows1.length > 0
							rows1.forEach (markets_db) ->
								exports.retailer[market].push (markets_db.name).replace(/amp\;/ig,'')
							doneCallback null,null
						else
							deferred.resolve exports.retailer
							doneCallback null,null
			),1000	
		exports.async.mapSeries markets, market_facet, (err, results) ->
			deferred.resolve (exports.retailer)
	),1000
	deferred.promise
	
exports.CacheBrandLogic = (retailer) ->
	#Create a promise
	deferred = exports.q.defer()
	exports.AllBrandKeyWords=[]
	setTimeout (->
		# console.log(exports.retailer)
		BrandLogic_qurey = "select tag_name from brand_keywords"
		# console.log "BrandLogic_qurey"+BrandLogic_qurey
		exports.connectToMysql()
		.then (mysqlConnection) ->
			mysqlConnection.query BrandLogic_qurey , (err1, rows1, fields1) ->
				#If the retailer exist in the database
				#Close mysql connection
				mysqlConnection.end()
				if err1
					mysqlConnection.end()
					deferred.reject err1
				else if rows1.length > 0
					rows1.forEach (keywords) ->
						exports.AllBrandKeyWords.push keywords.tag_name
					# console.log(exports.AllBrandKeyWords)
					deferred.resolve exports.retailer
				else
					deferred.resolve exports.retailer
	), 1000						
	deferred.promise	
	
exports.CacheTerms = () ->
	#Create a promise
	deferred = exports.q.defer()
	client = exports.redis.createClient(exports.redisConfig.port, exports.redisConfig.IP)
	#If redis is down throw an error
	client.on 'error', (err) ->
		deferred.reject new Error(err.code) + " -> Error connecting to redis " + exports.redisConfig.port 
	client.select 3, (err) ->
		setTimeout (->
			# console.log(exports.retailer)
			Term_count_qurey = "select count(e.id) from terms t join entities e on e.term_id=t.id"
			# console.log "BrandLogic_qurey"+BrandLogic_qurey
			exports.connectToMysql()
			.then (mysqlConnection) ->
				console.log(Term_count_qurey)
				mysqlConnection.query Term_count_qurey , (err1, rows1, fields1) ->
					#If the retailer exist in the database
					#Close mysql connection
					console.log("total row count==> "+Number(rows1[0]['count(e.id)']))
					if(Number(rows1[0]['count(e.id)']) != 0)
						total_count=Number((rows1[0]['count(e.id)']/100000).toFixed())+1
						console.log "total_count==>"+total_count
						Iteration_array=[1..total_count]
						console.log(Iteration_array)
						Iteration_Levels = (Levels, doneCallback) ->
							console.log("Levels==>"+Levels)
							start_range=Number(Levels-1)*100000
							console.log("start_range==>"+start_range)
							Term_qurey = "SELECT entities.id,entity_types.name,T.translation FROM entities LEFT JOIN entity_types ON entities.entity_type_id = entity_types.id LEFT JOIN terms T ON T.id = entities.term_id limit "+start_range+",100000"
							# Term_qurey = "SELECT entities.id,entity_types.name,T.translation FROM entities LEFT JOIN entity_types ON entities.entity_type_id = entity_types.id LEFT JOIN terms T ON T.id = entities.term_id limit 1,10"
							console.log(Term_qurey)
							mysqlConnection.query Term_qurey , (err2, rows2, fields2) ->
								# console.log(rows2)
								rows2.forEach (keywords) ->
									if(isNaN(keywords.translation))
										client.HSET((keywords.name).toLowerCase(),(keywords.translation).toLowerCase(),keywords.id)
										# client.set((keywords.translation).toLowerCase(),keywords.id)
									else
										client.HSET((keywords.name).toLowerCase(),keywords.translation,keywords.id)
										# client.set(keywords.translation,keywords.id)
								doneCallback null,null
						exports.async.mapSeries Iteration_array, Iteration_Levels, (err, results) ->
							console.log("ALL Items Completed In Terms")
							mysqlConnection.end()
							deferred.resolve null
		), 1000						
	deferred.promise
	
exports.CacheProduct = () ->
	#Create a promise
	deferred = exports.q.defer()
	client = exports.redis.createClient(exports.redisConfig.port, exports.redisConfig.IP)
	#If redis is down throw an error
	client.on 'error', (err) ->
		deferred.reject new Error(err.code) + " -> Error connecting to redis " + exports.redisConfig.port 
	client.select 4, (err) ->
		setTimeout (->
			# console.log(exports.retailer)
			Term_count_qurey = "select count(*) from products"
			# console.log "BrandLogic_qurey"+BrandLogic_qurey
			exports.connectToMysql()
			.then (mysqlConnection) ->
				console.log(Term_count_qurey)
				mysqlConnection.query Term_count_qurey , (err1, rows1, fields1) ->
					#If the retailer exist in the database
					#Close mysql connection
					console.log("total row count==> "+Number(rows1[0]['count(*)']))
					if(Number(rows1[0]['count(*)']) != 0)
						total_count=Number((rows1[0]['count(*)']/100000).toFixed())+1
						console.log "total_count==>"+total_count
						Iteration_array=[1..total_count]
						console.log(Iteration_array)
						Iteration_Levels = (Levels, doneCallback) ->
							console.log("Levels==>"+Levels)
							start_range=Number(Levels-1)*100000
							console.log("start_range==>"+start_range)
							Term_qurey = "select * from products limit "+start_range+",100000"
							console.log(Term_qurey)
							mysqlConnection.query Term_qurey , (err2, rows2, fields2) ->
								# console.log(rows2)
								rows2.forEach (keywords) ->
									client.HSET(keywords.legacy_product_key,'id',keywords.id)
									client.HSET(keywords.legacy_product_key,'name',keywords.name)
									client.HSET(keywords.legacy_product_key,'product_url',keywords.product_url)
									client.HSET(keywords.legacy_product_key,'brand',keywords.brand)
									client.HSET(keywords.legacy_product_key,'last_scrape_utc',keywords.last_scrape_utc)
									client.set((keywords.product_url).toLowerCase(),keywords.legacy_product_key)
									Name=keywords.name
									Brand=keywords.brand
									if(isNaN(keywords.name))
										client.set((keywords.name).toLowerCase(),keywords.legacy_product_key)
										Name=(keywords.name).toLowerCase()
									else
										client.set(keywords.name,keywords.legacy_product_key)
									if(isNaN(keywords.brand))
										Brand=(keywords.brand).toLowerCase()
									syle_str=Name+'_'+Brand
									client.set(syle_str,keywords.legacy_product_key)
								doneCallback null,null
						exports.async.mapSeries Iteration_array, Iteration_Levels, (err, results) ->
							console.log("ALL Items Completed In Products")
							mysqlConnection.end()
							deferred.resolve null
		), 1000						
	deferred.promise
	
exports.CacheSkus = () ->
	#Create a promise
	deferred = exports.q.defer()
	client = exports.redis.createClient(exports.redisConfig.port, exports.redisConfig.IP)
	#If redis is down throw an error
	client.on 'error', (err) ->
		deferred.reject new Error(err.code) + " -> Error connecting to redis " + exports.redisConfig.port 
	client.select 6, (err) ->
		setTimeout (->
			# console.log(exports.retailer)
			Term_count_qurey = "select count(*) from skus"
			# console.log "BrandLogic_qurey"+BrandLogic_qurey
			exports.connectToMysql()
			.then (mysqlConnection) ->
				console.log(Term_count_qurey)
				mysqlConnection.query Term_count_qurey , (err1, rows1, fields1) ->
					#If the retailer exist in the database
					#Close mysql connection
					console.log("total row count==> "+Number(rows1[0]['count(*)']))
					if(Number(rows1[0]['count(*)']) != 0)
						total_count=Number((rows1[0]['count(*)']/100000).toFixed())+1
						console.log "total_count==>"+total_count
						Iteration_array=[1..total_count]
						console.log(Iteration_array)
						Iteration_Levels = (Levels, doneCallback) ->
							console.log("Levels==>"+Levels)
							start_range=Number(Levels-1)*100000
							console.log("start_range==>"+start_range)
							Term_qurey = "select * from skus limit "+start_range+",100000"
							# Term_qurey = "select * from skus limit "+start_range+",10"
							console.log(Term_qurey)
							mysqlConnection.query Term_qurey , (err2, rows2, fields2) ->
								rows2.forEach (keywords) ->
									client.HSET(keywords.legacy_sku_key,'id',keywords.id)
									client.HSET(keywords.legacy_sku_key,'latest_price',keywords.latest_price)
								doneCallback null,null
						exports.async.mapSeries Iteration_array, Iteration_Levels, (err, results) ->
							console.log("ALL Items Completed In Skus")
							mysqlConnection.end()
							deferred.resolve null
		), 1000						
	deferred.promise

exports.get_retailergroup_ips = (groupname) ->
	# Create a promise
	console.log(groupname)
	# groupname='"'+groupname+'"'
	# console.log(groupname)
	deferred = exports.q.defer()
	# Init redis server_ip_client
	server_ip_client = exports.redis.createClient(exports.server_ip_client_redisConfig.port, exports.server_ip_client_redisConfig.IP)
	#If redis is down throw an error
	server_ip_client.on 'error', (err) ->
		console.log "Error here on get_retailergroup_ips"
		deferred.reject new Error(err.code) + " -> Error connecting to redis " 
	server_ip_client.select 5, (err) ->
		server_ip_client.smembers groupname, (err, result) ->
			exports.retailer_group_data=result
			deferred.resolve exports.retailer_group_data
	deferred.promise
	
# exports.translation = (Key,termbase,callback) ->	
	# deferred = exports.q.defer()
	# orginal_key=Key
	# country_value=country[exports.country_code]
	# keys=country_value+"_"+Key
	# Key=encodeURIComponent(Key)
	# if(country_value == 'spa')
		# termbase="57161a970cf2b005ed980bf2"
	# else if(country_value == 'ger')
		# termbase="5780b99c0cf2b007942dc8c5"
	# if(termbase == "")
		# JSON_DATA={text:Key,from:country_value,to:"eng"}
	# else
		# JSON_DATA={text:Key,from:country_value,to:"eng",termbaseIds:[termbase]}
	# url='https://lc-api.sdl.com/translate'
	# # translation_client = exports.redis.createClient(exports.translation_redisConfig.port, exports.translation_redisConfig.IP)
	# exports.translation_client.on 'error', (err) ->
		# deferred.resolve false
		# exports.errorLogger 'Error ' + err
		# process.exit 0
		# return
	# exports.translation_client.get keys ,(err, data) ->
		# if data
			# # exports.translation_client.unsubscribe()
			# callback data
		# else
			# exports.auth_translation={}
			# exports.auth_translation['headers']={}
			# exports.auth_translation['method']='POST'
			# exports.auth_translation['headers']['Content_Type']='application/json'
			# exports.auth_translation['headers']['Accept']='application/json'
			# exports.auth_translation['headers']['User-Agent']='Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'
			# exports.auth_translation['headers']['Authorization']=Sdl_Key
			# exports.auth_translation['json']=JSON_DATA
			# exports.download_translation url, 0,"trans",(data) ->
				# if(typeof(data) != 'object')
					# if(data.match(/ERR/i))
						# callback orginal_key
				# else if(data.translation)
					# exports.translation_client.set(keys,data.translation)
					# callback data.translation
	# deferred.promise
exports.translation = (Key,type,callback) ->	
	deferred = exports.q.defer()
	termbase=""
	orginal_key=Key
	country=(exports.country_code).toLowerCase()
	keys=exports.country_value+"_"+Key
	Key=encodeURIComponent(Key)
	console.log("keys==>"+keys)
	console.log("type==>"+type)
	exports.translation_client.on 'error', (err) ->
		deferred.resolve false
		exports.errorLogger 'Error ' + err
		process.exit 0
		return
	if(type == "SDL")
		url='https://www.googleapis.com/language/translate/v2?key=AIzaSyDHmlAOdmq65L59vfqpJyIfTBeqUrx9yck&q='+Key+'&source='+country+'&target=en&format=text'
		exports.translation_client.get keys ,(err, data) ->
			if data
				data=exports.entities.decodeHTML(data)
				console.log("=================================")
				console.log("SDL LIB")
				console.log(keys+"==>"+data)
				console.log("=================================")
				callback data
			else
				exports.translation_client.select 1, (err) ->
					exports.translation_client.get keys ,(err, data) ->
						if data
							data=exports.entities.decodeHTML(data)
							console.log("=================================")
							console.log("GOOGLE LIB")
							console.log(keys+"==>"+data)
							console.log("=================================")
							callback data
						else
							exports.auth_translation={}
							exports.auth_translation['headers']={}
							exports.auth_translation['method']='GET'
							exports.auth_translation['headers']['Content_Type']='application/json'
							exports.auth_translation['headers']['Accept']='application/json'
							exports.auth_translation['headers']['User-Agent']='Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'
							exports.auth_translation['json']=true
							exports.download_translation url, 0,"trans",(data) ->
								if(data['data'])
									if(data['data']['translations'])
										if(data['data']['translations'][0])
											if(data['data']['translations'][0]['translatedText'])
												translation_value=data['data']['translations'][0]['translatedText']
												translation_value=exports.entities.decodeHTML(translation_value)
											else
												callback orginal_key
										else
											callback orginal_key
									else
										callback orginal_key
								else
									callback orginal_key
								console.log(translation_value)
								if(typeof(data) != 'object')
									if(data.match(/ERR/i))
										callback orginal_key
								else if(translation_value)
									exports.translation_client.set(keys,translation_value)
									console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
									console.log("GOOGLE DOWN")
									console.log(keys+"==>"+translation_value)
									console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
									callback translation_value
	else
		keys=keys.toLowerCase()
			
		url='https://www.googleapis.com/language/translate/v2?key=AIzaSyDHmlAOdmq65L59vfqpJyIfTBeqUrx9yck&q='+Key+'&source='+country+'&target=en&format=text'
		exports.translation_client.select 1, (err) ->
			if(type == "update")
				exports.translation_client.del keys, (err, response) ->
					if response == 1
						console.log 'Deleted Successfully!'
					else
						console.log 'Cannot delete'
					exports.translation_client.get keys ,(err, data) ->
						if data
							data=exports.entities.decodeHTML(data)
							callback data
						else
							exports.auth_translation={}
							exports.auth_translation['headers']={}
							exports.auth_translation['method']='GET'
							exports.auth_translation['headers']['Content_Type']='application/json'
							exports.auth_translation['headers']['Accept']='application/json'
							exports.auth_translation['headers']['User-Agent']='Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'
							exports.auth_translation['json']=true
							exports.download_translation url, 0,"trans",(data) ->
								if(data['data'])
									if(data['data']['translations'])
										if(data['data']['translations'][0])
											if(data['data']['translations'][0]['translatedText'])
												translation_value=data['data']['translations'][0]['translatedText']
												translation_value=exports.entities.decodeHTML(translation_value)
											else
												callback orginal_key
										else
											callback orginal_key
									else
										callback orginal_key
								else
									callback orginal_key
								console.log(translation_value)
								if(typeof(data) != 'object')
									if(data.match(/ERR/i))
										callback orginal_key
								else if(translation_value)
									translation_value=translation_value.toLowerCase()
									exports.translation_client.set(keys,translation_value)
									console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
									console.log("GOOGLE DOWN")
									console.log(keys+"==>"+translation_value)
									console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
									callback translation_value
					
			else	
				exports.translation_client.get keys ,(err, data) ->
					if data
						data=exports.entities.decodeHTML(data)
						callback data
					else
						exports.auth_translation={}
						exports.auth_translation['headers']={}
						exports.auth_translation['method']='GET'
						exports.auth_translation['headers']['Content_Type']='application/json'
						exports.auth_translation['headers']['Accept']='application/json'
						exports.auth_translation['headers']['User-Agent']='Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'
						exports.auth_translation['json']=true
						exports.download_translation url, 0,"trans",(data) ->
							if(data['data'])
								if(data['data']['translations'])
									if(data['data']['translations'][0])
										if(data['data']['translations'][0]['translatedText'])
											translation_value=data['data']['translations'][0]['translatedText']
											translation_value=exports.entities.decodeHTML(translation_value)
										else
											callback orginal_key
									else
										callback orginal_key
								else
									callback orginal_key
							else
								callback orginal_key
							console.log(translation_value)
							if(typeof(data) != 'object')
								if(data.match(/ERR/i))
									callback orginal_key
							else if(translation_value)
								translation_value=translation_value.toLowerCase()
								exports.translation_client.set(keys,translation_value)
								console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
								console.log("GOOGLE DOWN")
								console.log(keys+"==>"+translation_value)
								console.log(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
								callback translation_value
	deferred.promise
#_______________________________________________________________________________
#	@desc download a url contents
#	@param url as web site url
#	@param trial count before give up and return error -- default = 5 = maxTrials
#	@return return html data	
exports.download = (url, trials,option, callback) ->
	deferred = exports.q.defer()
	#url assigned into authenticating JSON
	if(typeof url == "object")
		callback url
	else if(!url.match(/^htt/i))
		callback url
	else
		exports.auth['url']=url
		try
			# Luminati session changing
			if(exports.auth['proxy'])
				if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
					proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
					session_id = (1000000 * Math.random())|0
					proxy=proxy[1] + session_id + proxy[2]
					proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
					console.log("proxy::"+proxy)
					exports.auth['proxy']=proxy
				# netnut server changing
				else if(exports.auth['proxy'].match(/netnut/i))
					exports.auth['proxy']=exports.auth['proxy'].replace(/-s\d+/ig,'')
					proxy=exports.auth['proxy'].match(/(^[^>]*?)\.(netnut[^>]*?)$/i)
					rand=1
					if(exports.auth['proxy'].match(/\@us/i))
						rand=Math.floor(Math.random() * (150 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@uk/i))
						rand=Math.floor(Math.random() * (10 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@de/i))
						rand=Math.floor(Math.random() * (70 - 1)) + 1
					proxy=proxy[1]+"-s"+rand+"."+proxy[2]
					console.log("proxy::"+proxy)
					exports.auth['proxy']=proxy
			# console.log(exports.auth)
			if(exports.auth['headers']['Accept-Encoding'])
				req = exports.request.get(exports.auth)
				# req.pipe(fs.createWriteStream('zlib_zip_content.html'))
				req.on 'response', (res) ->
					# if(res.statusCode != 200)
						# deferred.reject
					formatDate("download: " + url,res.statusCode ,option )
					# console.log("URL===>"+url+"::"+res.statusCode)
					# fs.writeFileSync('zlib_responce.txt' , JSON.stringify(res))
					# if(res.statusCode == 200)
					chunks = []
					res.on 'data', (chunk) ->
						chunks.push chunk
						return
					res.on 'error', (err) ->
						if ++trials <= maxTrials
							if(exports.auth['proxy'])
								if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth['proxy']=proxy
							exports.download url, trials,option, callback
						else
							deferred.reject new Error(err)
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
					res.on 'end', ->
						# if(res.statusCode == 200)
						# oneGigInBytes = 1073741824
						oneGigInBytes = 2073741824
						buffer_size = oneGigInBytes-1
						# buffer = Buffer.alloc(buffer_size)
						# buffer = new Buffer(buffer_size)
						# console.log buffer.length
						
						# console.log buffer
						encoding = res.headers['content-encoding']
						try
							if encoding == 'gzip' and res.statusCode == 200
								console.log "GZIP IF"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.gunzip buffer, (err, decoded) ->
									if err
										console.log err
									# console.log decoded
									callback decoded and decoded.toString()
									return
							else if encoding == 'deflate' and res.statusCode == 200
								console.log "GZIP DEFLATE"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.inflate buffer, (err, decoded) ->
									callback decoded and decoded.toString()
									return
							else
								console.log "GZIP ELSE"
								callback chunks.toString()
						catch e1
							deferred.reject new Error(e1)
					# else
						# deferred.reject
				req.on 'error', (err1) ->
					deferred.reject new Error(err1)
			else
				exports.request exports.auth, (err, res,data) ->
					if res
						formatDate("download: " + url,res.statusCode ,option )
					else
						formatDate("download: " + url,"No statusCode",option )
					if(option == 'trans' and res.statusCode == 500)
						callback "ERR"
					if err
						if ++trials <= maxTrials
							if(exports.auth['proxy'])
								if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth['proxy']=proxy
							exports.download url, trials,option, callback
						else
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
							if(option =='detail')
								callback err
					else
						if(res.statusCode != 500)
							if callback and typeof callback == 'function'
								callback data
							else
								if(option =='detail')
									console.log(data)
									callback data
								else
									deferred.resolve data
						else
							if(option =='detail')
								console.log("500===>"+data)
								callback data
							else
								deferred.resolve data
					return
		catch e
			console.log "Error"+e
			deferred.reject new Error(e)
	deferred.promise

exports.download_responce = (url, trials,option, callback) ->
	deferred = exports.q.defer()
	#url assigned into authenticating JSON
	content={}
	content['content']={}
	content['res']={}
	if(typeof url == "object")
		callback url
	else if(!url.match(/^htt/i))
		callback url
	else
		exports.auth['url']=url
		try
			# Luminati session changing
			if(exports.auth['proxy'])
				if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
					proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
					session_id = (1000000 * Math.random())|0
					proxy=proxy[1] + session_id + proxy[2]
					proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
					console.log("proxy::"+proxy)
					exports.auth['proxy']=proxy
				# netnut server changing
				else if(exports.auth['proxy'].match(/netnut/i))
					exports.auth['proxy']=exports.auth['proxy'].replace(/-s\d+/ig,'')
					proxy=exports.auth['proxy'].match(/(^[^>]*?)\.(netnut[^>]*?)$/i)
					rand=1
					if(exports.auth['proxy'].match(/\@us/i))
						rand=Math.floor(Math.random() * (150 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@uk/i))
						rand=Math.floor(Math.random() * (10 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@de/i))
						rand=Math.floor(Math.random() * (70 - 1)) + 1
					proxy=proxy[1]+"-s"+rand+"."+proxy[2]
					console.log("proxy::"+proxy)
					exports.auth['proxy']=proxy
			# console.log(exports.auth)
			if(exports.auth['headers']['Accept-Encoding'])
				req = exports.request.get(exports.auth)
				# req.pipe(fs.createWriteStream('zlib_zip_content.html'))
				req.on 'response', (res) ->
					# if(res.statusCode != 200)
						# deferred.reject
					content['res']=res
					formatDate("download: " + url,res.statusCode ,option )
					# console.log("URL===>"+url+"::"+res.statusCode)
					# fs.writeFileSync('zlib_responce.txt' , JSON.stringify(res))
					# if(res.statusCode == 200)
					chunks = []
					res.on 'data', (chunk) ->
						chunks.push chunk
						return
					res.on 'error', (err) ->
						if ++trials <= maxTrials
							if(exports.auth['proxy'])
								if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth['proxy']=proxy
							exports.download url, trials,option, callback
						else
							deferred.reject new Error(err)
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
					res.on 'end', ->
						# if(res.statusCode == 200)
						# oneGigInBytes = 1073741824
						oneGigInBytes = 2073741824
						buffer_size = oneGigInBytes-1
						# buffer = Buffer.alloc(buffer_size)
						# buffer = new Buffer(buffer_size)
						# console.log buffer.length
						
						# console.log buffer
						encoding = res.headers['content-encoding']
						try
							if encoding == 'gzip' and res.statusCode == 200
								console.log "GZIP IF"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.gunzip buffer, (err, decoded) ->
									if err
										console.log err
									# console.log decoded
									content['content']=decoded and decoded.toString()
									# callback decoded and decoded.toString()
									callback content
									return
							else if encoding == 'deflate' and res.statusCode == 200
								console.log "GZIP DEFLATE"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.inflate buffer, (err, decoded) ->
									content['content']=decoded and decoded.toString()
									# callback decoded and decoded.toString()
									callback content
									return
							else
								console.log "GZIP ELSE"
								content['content']=chunks.toString()
								# callback chunks.toString()
								callback content
						catch e1
							deferred.reject new Error(e1)
					# else
						# deferred.reject
				req.on 'error', (err1) ->
					deferred.reject new Error(err1)
			else
				exports.request exports.auth, (err, res,data) ->
					content['content']=data
					content['res']=res
					if res
						formatDate("download: " + url,res.statusCode ,option )
					else
						formatDate("download: " + url,"No statusCode",option )
					if(option == 'trans' and res.statusCode == 500)
						callback "ERR"
					if err
						if ++trials <= maxTrials
							if(exports.auth['proxy'])
								if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth['proxy']=proxy
							exports.download url, trials,option, callback
						else
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
							if(option =='detail')
								callback err
					else
						if(res.statusCode != 500)
							if callback and typeof callback == 'function'
								# callback data
								callback content
							else
								if(option =='detail')
									console.log(data)
									# callback data
									callback content
								else
									deferred.resolve data
						else
							if(option =='detail')
								console.log("500===>"+data)
								# callback data
								callback content
							else
								deferred.resolve data
					return
		catch e
			console.log "Error"+e
			deferred.reject new Error(e)
	deferred.promise
	
exports.download_translation = (url, trials,option, callback) ->
	deferred = exports.q.defer()
	#url assigned into auth_translationenticating JSON
	if(typeof url == "object")
		callback url
	else if(!url.match(/^htt/i))
		callback url
	else
		exports.auth_translation['url']=url
		try
			# Luminati session changing
			if(exports.auth_translation['proxy'])
				if(exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
					proxy=exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
					session_id = (1000000 * Math.random())|0
					proxy=proxy[1] + session_id + proxy[2]
					proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
					console.log("proxy::"+proxy)
					exports.auth_translation['proxy']=proxy
				# netnut server changing
				else if(exports.auth['proxy'].match(/netnut/i))
					exports.auth['proxy']=exports.auth['proxy'].replace(/-s\d+/ig,'')
					proxy=exports.auth['proxy'].match(/(^[^>]*?)\.(netnut[^>]*?)$/i)
					rand=1
					if(exports.auth['proxy'].match(/\@us/i))
						rand=Math.floor(Math.random() * (150 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@uk/i))
						rand=Math.floor(Math.random() * (10 - 1)) + 1
					else if(exports.auth['proxy'].match(/\@de/i))
						rand=Math.floor(Math.random() * (70 - 1)) + 1
					proxy=proxy[1]+"-s"+rand+"."+proxy[2]
					console.log("proxy::"+proxy)
					exports.auth['proxy']=proxy
			# console.log(exports.auth_translation)
			if(exports.auth_translation['headers']['Accept-Encoding'])
				req = exports.request.get(exports.auth_translation)
				# req.pipe(fs.createWriteStream('zlib_zip_content.html'))
				req.on 'response', (res) ->
					# if(res.statusCode != 200)
						# deferred.reject
					formatDate("download: " + url,res.statusCode ,option )
					# console.log("URL===>"+url+"::"+res.statusCode)
					# fs.writeFileSync('zlib_responce.txt' , JSON.stringify(res))
					# if(res.statusCode == 200)
					chunks = []
					res.on 'data', (chunk) ->
						chunks.push chunk
						return
					res.on 'error', (err) ->
						if ++trials <= maxTrials
							if(exports.auth_translation['proxy'])
								if(exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth_translation['proxy']=proxy
							exports.download url, trials,option, callback
						else
							deferred.reject new Error(err)
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
					res.on 'end', ->
						# if(res.statusCode == 200)
						# oneGigInBytes = 1073741824
						oneGigInBytes = 2073741824
						buffer_size = oneGigInBytes-1
						# buffer = Buffer.alloc(buffer_size)
						# buffer = new Buffer(buffer_size)
						# console.log buffer.length
						
						# console.log buffer
						encoding = res.headers['content-encoding']
						try
							if encoding == 'gzip' and res.statusCode == 200
								console.log "GZIP IF"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.gunzip buffer, (err, decoded) ->
									if err
										console.log err
									# console.log decoded
									callback decoded and decoded.toString()
									return
							else if encoding == 'deflate' and res.statusCode == 200
								console.log "GZIP DEFLATE"
								buffer = Buffer.concat(chunks)
								console.log buffer.length
								exports.zlib.inflate buffer, (err, decoded) ->
									callback decoded and decoded.toString()
									return
							else
								console.log "GZIP ELSE"
								callback chunks.toString()
						catch e1
							deferred.reject new Error(e1)
					# else
						# deferred.reject
				req.on 'error', (err1) ->
					deferred.reject new Error(err1)
			else
				exports.request exports.auth_translation, (err, res,data) ->
					if res
						formatDate("download: " + url,res.statusCode ,option )
					else
						formatDate("download: " + url,"No statusCode",option )
					if(option == 'trans' and res.statusCode == 500)
						callback "ERR"
					if(res.statusCode != 200)
						if ++trials <= maxTrials
							if(exports.auth_translation['proxy'])
								if(exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth_translation['proxy']=proxy
							exports.download url, trials,option, callback
					if err
						if ++trials <= maxTrials
							if(exports.auth_translation['proxy'])
								if(exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
									proxy=exports.auth_translation['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
									session_id = (1000000 * Math.random())|0
									session_id++
									console.log("session_id::"+session_id)
									proxy=proxy[1] + session_id + proxy[2]
									proxy=proxy.replace(/superproxy/ig,exports.Super_proxy)
									console.log("proxy::"+proxy)
									exports.auth_translation['proxy']=proxy
							exports.download url, trials,option, callback
						else
							console.log 'Error fetching: ' + url
							console.log err
							exports.errorLogger 'Error fetching: ' + url
							exports.errorLogger err
							if(option =='detail')
								callback err
					else
						if(res.statusCode != 500)
							if callback and typeof callback == 'function'
								callback data
							else
								if(option =='detail')
									console.log(data)
									callback data
								else
									deferred.resolve data
						else
							if(option =='detail')
								console.log("500===>"+data)
								callback data
							else
								deferred.resolve data
					return
		catch e
			console.log "Error"+e
			deferred.reject new Error(e)
	deferred.promise
	
exports.download_new = (url, trials,option, callback) ->
	deferred = exports.q.defer()
	if(url.match(/^http/i))
		#url assigned into authenticating JSON
		exports.auth['url']=url
		# Luminati session changing
		if(exports.auth['proxy'])
			if(exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i))
				proxy=exports.auth['proxy'].match(/(^[^>]*?session\-)[^>]*?(\:[^>]*?)$/i)
				session_id = (1000000 * Math.random())|0
				proxy=proxy[1] + session_id + proxy[2]
				exports.auth['proxy']=proxy
				console.log(exports.auth['proxy'])
				# netnut server changing
			else if(exports.auth['proxy'].match(/netnut/i))
				exports.auth['proxy']=exports.auth['proxy'].replace(/-s\d+/ig,'')
				proxy=exports.auth['proxy'].match(/(^[^>]*?)\.(netnut[^>]*?)$/i)
				rand=1
				if(exports.auth['proxy'].match(/\@us/i))
					rand=Math.floor(Math.random() * (150 - 1)) + 1
				else if(exports.auth['proxy'].match(/\@uk/i))
					rand=Math.floor(Math.random() * (10 - 1)) + 1
				else if(exports.auth['proxy'].match(/\@de/i))
					rand=Math.floor(Math.random() * (70 - 1)) + 1
				proxy=proxy[1]+"-s"+rand+"."+proxy[2]
				console.log("proxy::"+proxy)
				exports.auth['proxy']=proxy
		exports.request exports.auth, (err, res,data) ->
			if res
				formatDate("download: " + url,res.statusCode ,option )
			if err
				if ++trials <= maxTrials
					exports.download url, trials,option, callback
				else
					console.log 'Error fetching: ' + url
					console.log err
					exports.errorLogger 'Error fetching: ' + url
					exports.errorLogger err
					if(option =='detail')
						callback err
			else
				if(res.statusCode != 500)
					if callback and typeof callback == 'function'
						callback data
					else
						if(option =='detail')
							callback data
						else
							deferred.resolve data
				else
					if(option =='detail')
						callback data
					else
						deferred.resolve data
			return
	else
		callback url
	deferred.promise
	

#_______________________________________________________________________________

#--- Development only
#--- Just output a time log 
formatDate = (text,status,option) ->
	date = new Date
	hours = date.getHours()
	minutes = date.getMinutes()
	seconds = date.getSeconds()
	ampm = if hours >= 12 then 'pm' else 'am'
	hours = hours % 12
	hours = if hours then hours else 12
	minutes = if minutes < 10 then '0' + minutes else minutes
	strTime = hours + ':' + minutes + ':' + seconds + ' ' + ampm
	unless(option == "trans")
		exports[option+'Logger'] '=>' , text ,  status , ' time ' + date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + '  ' + strTime
	console.log '=>' , text, status, ' time ' + date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + '  ' + strTime
	return

exports.json_converter = (str) ->
	eval('var JSON_data='+str)
	return JSON_data 
	
# @getmd5: This get source content from redis for respective md5 file 
# return source content to retailer script 
exports.getmd5 = (file,callback) ->
	deferred = exports.q.defer()
	#Establishing redis connection
	common_client1 = exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
	common_client1.on 'error', (err) ->
		deferred.resolve false
		exports.errorLogger 'Error ' + err
		process.exit 0
		return
	#change redis DB 
	common_client1.select 2, (err) ->
		#Get the content from redis
		common_client1.get file ,(err, data) ->
			
			if callback and typeof callback == 'function'
				common_client1.quit()
				# exports.common_client.unsubscribe()
				callback data
			else
				# exports.common_client.unsubscribe()
				common_client1.quit()
				deferred.resolve data
	deferred.promise


#_______________________________________________________________________________
#	@desc assign product_categories, product_facet values from redis
#	@param Binding param @productObj as product object;
#	@return return array of products urls
#mergeTags
translationDetail = () ->
	# Create a promise
	deferred = exports.q.defer()
	console.log("translationDetail")
	# product Object from addProduct function
	translation_update=""
	productObj = @productObj
	console.log(productObj.product)
	if(productObj['translation_update'])
		translation_update="update"
	if(productObj['translation'])
		if(productObj['translation'] == true)
			image_filename=productObj.product.image_filename
			mainTerms = (mainkey, Callback) ->
				if(mainkey == "product")
					productTerms = (section, Callback1) ->
						# if(section.match(/name|description_overview|materials_raw_text|description_details/ig))
						if(section.match(/name|description_overview|description_details/ig))
							if(!section.match(/image_filename/ig))
								value=productObj.product[section]
								if(value != "")
									if(productObj['translation_type'])
										exports.translation value,"SDL", (data_valus) ->
											delete productObj.product[section]
											productObj.product[section]=data_valus
											Callback1(null, productObj)
									else
										exports.translation value,translation_update, (data_valus) ->
											delete productObj.product[section]
											productObj.product[section]=data_valus
											Callback1(null, productObj)
								else
									Callback1(null, productObj)
							else
								Callback1(null, productObj)
						else if(section.match(/tag/ig))
							value=productObj.product[section]
							delete productObj.product[section]
							total_tag_after_trans=[]
							total_tga=value.split(exports.splitter)
							console.log(total_tga)
							all_tag_tr = (tag_str, Callback_tag) ->
								tag_str_arr=tag_str.split('=')
								str_count=0
								tag_str_menu=''
								main_tag_str=""
								value_str = (single_str, Callback_val) ->
									if(str_count == 0)
										str_count++
										if(single_str.match(/menu/i))
											tag_str_menu=single_str
											Callback_val(null,null)
										else
											if(isNaN(single_str))
												if(productObj['translation_type'])
													exports.translation single_str,"SDL", (data_valus) ->
														tag_str_menu=data_valus
														Callback_val(null,null)
												else
													exports.translation single_str,translation_update, (data_valus) ->
														tag_str_menu=data_valus
														Callback_val(null,null)
											else
												tag_str_menu=single_str
												Callback_val(null,null)
									else
										str_count++
										if(tag_str_menu.match(/brand/i))
											main_tag_str=tag_str_menu+'='+single_str
											total_tag_after_trans.push(main_tag_str)
											Callback_val(null,null)
										else
											if(isNaN(single_str))
												if(productObj['translation_type'])
													exports.translation single_str,"SDL", (data_valus) ->
														main_tag_str=tag_str_menu+'='+data_valus
														total_tag_after_trans.push(main_tag_str)
														Callback_val(null,null)
												else
													exports.translation single_str,translation_update, (data_valus) ->
														main_tag_str=tag_str_menu+'='+data_valus
														total_tag_after_trans.push(main_tag_str)
														Callback_val(null,null)												
											else
												main_tag_str=tag_str_menu+'='+single_str
												total_tag_after_trans.push(main_tag_str)
												Callback_val(null,null)
								exports.async.mapSeries (tag_str_arr), value_str, (err, results) ->
									Callback_tag(null,null)
							exports.async.mapSeries (total_tga), all_tag_tr, (err, results) ->
								final_tag_str=total_tag_after_trans.join(exports.splitter)
								productObj.product[section]=final_tag_str
								Callback1(null, productObj)
						else
							Callback1(null, productObj)
					exports.async.mapSeries Object.keys(productObj[mainkey]), productTerms, (err, results) ->
						productObj.product.image_filename=image_filename
						Callback(null, productObj)
						return
				else if(mainkey == "skuHistory")
					# console.log(productObj[mainkey])
					skuTerms = (section, Callback1) ->
						Terms = (section1, Callback2) ->
							key=productObj[mainkey][section][1][section1][0]
							value=productObj[mainkey][section][1][section1][1]
							productObj[mainkey][section][1][section1][2]=productObj[mainkey][section][1][section1][1]
							if(key == 'size')
								# if(isNaN(value))
								# if(value.length >= 10)
								if(productObj['translation_type'])
									if(value.length >= 10)
										exports.translation value,"SDL", (data_valus) ->
											delete productObj[mainkey][section][1][section1][1]
											productObj[mainkey][section][1][section1][1]=data_valus
											Callback2(null, productObj)
									else
										Callback2(null, productObj)
								else
									if(isNaN(value))
										exports.translation value,translation_update, (data_valus) ->
											delete productObj[mainkey][section][1][section1][1]
											productObj[mainkey][section][1][section1][1]=data_valus
											Callback2(null, productObj)
									else
										Callback2(null, productObj)
								# else
									# Callback2(null, productObj)
							else if(key == 'color')
								if(value.match(/No raw color/i))
									Callback2(null, productObj)
								else
									if(productObj['translation_type'])
										exports.translation value,"SDL", (data_valus) ->
											delete productObj[mainkey][section][1][section1][1]
											productObj[mainkey][section][1][section1][1]=data_valus
											Callback2(null, productObj)
									else
										exports.translation value,translation_update, (data_valus) ->
											delete productObj[mainkey][section][1][section1][1]
											productObj[mainkey][section][1][section1][1]=data_valus
											Callback2(null, productObj)
						exports.async.mapSeries Object.keys(productObj[mainkey][section][1]), Terms, (err, results) ->
							Callback1(null, productObj)
							return
					exports.async.mapSeries Object.keys(productObj[mainkey]), skuTerms, (err, results) ->
						Callback(null, productObj)
						return
				else
					Callback(null, productObj)
			exports.async.mapSeries Object.keys(productObj), mainTerms, (err, results) ->
				deferred.resolve productObj
				return
		else
			deferred.resolve productObj
	else
		deferred.resolve productObj
		
	deferred.promise
# Brand Logic
BrandLogic = () ->
	# Create a promise
	deferred = exports.q.defer()
	# product Object from addProduct function
	console.log("BrandLogic")
	productObj = @productObj
	length_AllBrandKeyWords=(exports.AllBrandKeyWords).length
	console.log(length_AllBrandKeyWords)
	if(length_AllBrandKeyWords != 0)
		brandChilds = (keywords, callback) ->
			# productObj.product.tag=(productObj.product.tag).replace(RegExp('^\s*#{keywords}\s*$','ig'),'Brand')
			productObj.product.tag=(productObj.product.tag).replace(new RegExp("¶\s*#{keywords}\s*=",'ig'),'¶Brand=')
			productObj.product.tag=(productObj.product.tag).replace(new RegExp("^\s*#{keywords}\s*=",'ig'),'Brand=')
			# .replace(new RegExp("¶\s*#{keywords}\s*=",'ig'),'¶Brand=')
			callback null,null
		exports.async.mapSeries exports.AllBrandKeyWords, brandChilds, (err, results) ->
			if(productObj.product.brand != '' and !((productObj.product.tag).match(/Brand/i)))
				productObj.product.tag=productObj.product.tag+'¶brand='+productObj.product.brand
			else if(productObj.product.brand == '' and (productObj.product.tag).match(/Brand\=([^>]*?)($|\¶)/i))
				productObj.product.brand=((productObj.product.tag).match(/Brand\=([^>]*?)($|\¶)/i))[1]
			else if(productObj.product.brand == '' and !((productObj.product.tag).match(/Brand/i)))
				own_brand=(exports.retailer.retailer_code).replace(/\-[^>]*?$/ig,'')
				productObj.product.tag=productObj.product.tag+'¶brand='+own_brand
				productObj.product.brand=own_brand
			productObj.product.tag=(productObj.product.tag).replace("¶¶","¶")
			deferred.resolve productObj
	else 
		deferred.resolve productObj
	return deferred.promise
	
getCategoriesFacetsFromRedis = () ->
	# Create a promise
	deferred = exports.q.defer()
	# product Object from addProduct function
	productObj = @productObj
	Tag=[]
	temp_tag=[]
	# Init redis client
	console.log("getCategoriesFacetsFromRedis")
	console.log(productObj.product)
	product_name=productObj.product.name
	product_name=product_name.replace(/^\**|\**|\.*/ig,'')
	product_name=product_name.replace(/\s+/ig,' ')
	productObj.product.name=product_name
	# exports.client.smembers productObj.product.product_url, (err, result) ->
	exports.client.select 0, (err) ->
		exports.client.smembers productObj.product.product_url, (err, result) ->
			result.forEach (tagList) ->
				tagList = tagList.split(exports.splitter)
				tagListArray = tagList[1].split(",")
				if tagList[0].toLowerCase() == 'category'
					tagListArray.forEach (Menus) ->
						Menus=Menus.replace(/\§/i,",")
						Menus_1=Menus.toLowerCase()
						# Menus='category='+Menus
						unless(Menus_1 in temp_tag)
							Tag.push(Menus)
							temp_tag.push(Menus_1)
				else if tagList[0].toLowerCase() == 'facet'
					Menus=tagListArray[0]+'='+tagListArray[1]
					Menus_1=Menus.toLowerCase()
					unless(Menus_1 in temp_tag)
						Tag.push(Menus)
						temp_tag.push(Menus_1)
				return
			# exports.client.unsubscribe()
			# Return product Object
			product_Tag=Tag.join(exports.splitter)
			productObj.product["tag"] = product_Tag
			deferred.resolve productObj
			return
	deferred.promise
	
#_______________________________________________________________________________

currencyValue = (value) ->
	if value == null or value.length == 0
		return null
		
	return Number(value.replace /[^0-9\.]+/g, '')

	
#_______________________________________________________________________________
#	@desc add products sku history to database; if sku history changed.
#	@param Binding param @productObj as retailer object; which has SKU matrix; 
#	@param Binding @mysqlConnection as mysql connection
#	@return id of the inserted record or id of the current record if exists.

addSkuHistory = () ->
	#create a promise 
	deferred = exports.q.defer()
	# mysql connection from transact
	mysqlConnection = @mysqlConnection
	# product Object from addProduct function
	productObj = @productObj
	console.log("addSkuHistory")
	# console.log(productObj.skuHistory)
	# Check for duplicate products 
	if (productObj.product_duplicate == false )
		product_already_exist=productObj.product_already_exist
		skuHistory = (skuIndex, doneCallback) ->
			priceNow = productObj.skuHistory[skuIndex][3]
			priceWas = productObj.skuHistory[skuIndex][4]
			stock=productObj.skuHistory[skuIndex][5]
			price = currencyValue priceNow
			if priceWas.length > 0
				originalPrice = Number(priceWas.replace(/[^0-9\.]+/g, ''))
				originalPriceUtc = exports.reportingYesterdayDate
			else if priceNow.length > 0
				originalPrice = Number(priceNow.replace(/[^0-9\.]+/g, ''))
				originalPriceUtc = exports.reportingDate
			else
				originalPrice = null
				originalPriceUtc = exports.reportingYesterdayDate
			SKU = 
				product_gold_key : productObj.product.product_gold_key
				sku_gold_key: productObj.skuHistory[skuIndex]['skuGoldKey']
				price_was: originalPrice
				price_now: price
				is_in_stock: productObj.skuHistory[skuIndex][5] == 'true' or productObj.skuHistory[skuIndex][5] == true		
			if(product_already_exist == false)
				if(stock == true)
					mysqlConnection.query 'INSERT INTO sku_history_gold SET ?', SKU, (err, result) ->
						if !err
							doneCallback null, null
							return
						else
							console.log "Error addSkuHistory - insert" + err
							doneCallback null, null
							# deferred.reject new Error(err) + " -> Error addSkuHistory - insert"
				else
					doneCallback null, null
					return
			else 	
				mysqlConnection.query 'INSERT INTO sku_history_gold SET ?', SKU, (err, result) ->
					if !err
						doneCallback null, null	
						return
					else
						console.log "Error addSkuHistory - insert" + err
						doneCallback null, null
						# deferred.reject new Error(err) + " -> Error addSkuHistory - insert"
						
		# # Loop through productObj.skuHistory keys
		exports.async.map Object.keys(productObj.skuHistory), skuHistory, (err, results) ->
			deferred.resolve null
			return
	else
		deferred.resolve productObj
		
	deferred.promise


# deletes all sku and product source content for every single product.
dele_md5_file = () ->
	#create a promise 
	deferred = exports.q.defer()
	# product Object from addProduct function
	productObj = @productObj
	#Establishing redis connection
	console.log("dele_md5_file")
	if(!productObj.delete_md5)
		common_client1 = exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
		common_client1.on 'error', (err) ->
			deferred.resolve false
			exports.errorLogger 'Error ' + err
			process.exit 0
			return
		dele_md5 = (md5_file, doneCallback) ->
			#change redis DB 
			console.log(md5_file)
			common_client1.select 2, (err) ->
				#Delete content from redis for respective md5 file.
				common_client1.del md5_file, (err, reply) ->
					doneCallback null, null
				return
		exports.async.map Object.keys(productObj.md5_files), dele_md5, (err, results) ->
			# exports.common_client.unsubscribe()
			common_client1.quit()
			console.log("Completed")
			deferred.resolve null
			return
	else
		console.log("dele_md5_file222")
		deferred.resolve null
	deferred.promise


exports.shuffle = (array) ->
	counter = array.length
	# While there are elements in the array
	while counter > 0
		# Pick a random index
		index = Math.floor(Math.random() * counter)
		# Decrease counter by 1
		counter--
		# And swap the last element with it
		temp = array[counter]
		array[counter] = array[index]
		array[index] = temp
	return array

#_______________________________________________________________________________
#	generateUUID string
#	generates Md5 key
#	@return md5 string(UUID)
	
generateUUID = (str) ->
	UUID = "N/A"
	if str.length > 0
		hash = md5 str
		hex_high_10 =
		  '0': '8'
		  '1': '9'
		  '2': 'a'
		  '3': 'b'
		  '4': '8'
		  '5': '9'
		  '6': 'a'
		  '7': 'b'
		  '8': '8'
		  '9': '9'
		  'a': 'a'
		  'b': 'b'
		  'c': '8'
		  'd': '9'
		  'e': 'a'
		  'f': 'b'
		UUID = hash.substr(0, 8) + '-' + hash.substr(8, 4) + '-' + '3' + hash.substr(13, 3) + '-' + hex_high_10[hash.substr(16, 1)] + hash.substr(17, 1) + hash.substr(18, 2) + '-' + hash.substr(20, 12)  
	if UUID == "N/A" 
		console.log "report a problem: " + str
	
	return UUID
	
#_______________________________________________________________________________
#	@desc add product in the database if exist update last_scrape_utc
#	@param Binding param @productObj as retailer object
#	@param Binding @mysqlConnection as mysql connection
#	@return

addProduct = () ->
	# Create a promise
	deferred = exports.q.defer()
	# mysql connection from transact
	mysqlConnection = @mysqlConnection
	console.log("addProduct")
	
	# Product object from scrapeTheProducts function
	productObj = @productObj
	productObj.product["tag"]=(productObj.product["tag"]).toLowerCase()
	soldOutArray = []
	Object.keys(productObj.skuHistory).forEach (index) ->
		soldOutArray.push productObj.skuHistory[index][5]
		
	# Checking the sold out product
	soldOut = soldOutArray.indexOf(true) == -1
	console.log(soldOut)
	tag=exports.splitter+productObj.product.tag
	exports.client.select 7, (err) ->
		exports.client.exists productObj.product.product_gold_key, (err, reply) ->
			if (reply == 1)
				exports.client.select 7, (err) ->
					exports.client.get productObj.product.product_gold_key, (err, result) ->
						console.log(result)
						if(productObj['pro_dup'])
							productObj.product_duplicate = false
							productObj.product_already_exist = true
						else if(productObj.isStyleMerging == "Name" or productObj.isStyleMerging == "Name and Brand")
							productObj.product_duplicate = false
						else
							productObj.product_duplicate = true
						protag=productObj.product.tag
						own_brand=(exports.retailer.retailer_code).replace(/\-[^>]*?$/ig,'')
						own_brand=own_brand.toLowerCase()
						if(result.match(/brand\=([^>]*?)(?:\¶|$)/i))
							brand_tag=result.match(/brand\=([^>]*?)(?:\¶|$)/i)[1]
							brand_tag=brand_tag.toLowerCase()
							if(brand_tag == own_brand)
								if(protag.match(/brand\=([^>]*?)(?:\¶|$)/i))
									brand_tag=protag.match(/brand\=([^>]*?)(?:\¶|$)/i)[1]
									result=result.replace(/\¶brand\=[^>]*?$/ig,'')
									result=result.replace(/\¶brand\=[^>]*?\¶/ig,'¶')
									brand_tag=brand_tag.toLowerCase()
						tag_array=result.split(exports.splitter)
						product_array=productObj.product.tag.split(exports.splitter)
						product_array.forEach (Menus) ->
							unless(Menus in tag_array)
								tag_array.push(Menus)
						new_tag_arry=[]
						tag_objects={}
						console.log(tag_array)
						tag_array.forEach (tag_value) ->
							tag_value=tag_value.toLowerCase()
							unless(tag_objects[tag_value])
								new_tag_arry.push(tag_value)
								tag_objects[tag_value]=tag_value
						tag=new_tag_arry.join(exports.splitter).toLowerCase()
						exports.client.set(productObj.product.product_gold_key,tag)
						console.log("---------------------------------------------------------")
						console.log(productObj.product.product_gold_key,tag)
						console.log("---------------------------------------------------------")
						#D Count update.
						exports.client.select 0, (err) ->
							exports.client.incr "d_count"
						sql ="update product_gold set tag =" + mysqlConnection.escape(tag) + ", brand=" + mysqlConnection.escape(brand_tag) + "where product_gold_key = " + mysqlConnection.escape(productObj.product.product_gold_key)
						mysqlConnection.query sql, (err, result) ->
							if !err
								deferred.resolve productObj
							else
								console.log(err)
								deferred.reject new Error(err) + " -> Error addProduct - concat"
			else
				productObj.product_duplicate = false
				console.log("NO DUP")
				exports.client.select 4, (err) ->
					console.log(productObj.product.product_gold_key)
					exports.client.hexists productObj.product.product_gold_key,'id', (err, old_reply) ->
						if !err
							console.log(old_reply)
							# Product is not in the database -> add it, set product_already_exist to false, update first_scrape_utc, last_scrape_utc
							if old_reply != 1
								productObj['default_image']=productObj.product.image_filename
								productObj.product.image_filename = crypto.createHash('md5').update(productObj.product.image_filename).digest('hex').toUpperCase()+'.jpg'
								# Add prouct to products table
								if(!soldOut and productObj.product_style == "New")
									legacy_product_key = productObj.product.product_gold_key
									id=0
									name = (productObj.product.name).toLowerCase()
									brand = (productObj.product.brand).toLowerCase()
									product_url = productObj.product.product_url
									syle_str=name+'_'+brand
									exports.client.select 4, (err) ->
										exports.client.HSET(legacy_product_key,'id',id)
										exports.client.HSET(legacy_product_key,'name',name)
										exports.client.HSET(legacy_product_key,'product_url',product_url)
										exports.client.HSET(legacy_product_key,'brand',brand)
										exports.client.set(name,legacy_product_key)
										exports.client.set(syle_str,legacy_product_key)
								if !soldOut and productObj.isStyleMerging == "NO" 
									console.log("productObj.isStyleMerging == NO new product ")
									mysqlConnection.query 'INSERT INTO product_gold SET ?', productObj.product, (err1, result1) ->
										if err1
											console.log "addProduct - insert " + err1
											return deferred.resolve productObj
											# deferred.reject new Error(err1) + " -> Error addProduct - insert"
										else 
											productObj.product.id = result1.insertId
											productObj.product_already_exist = false
											if(productObj['pro_dup'])
												productObj.product_duplicate = false
												productObj.product_already_exist = true											
											exports.client.select 7, (err) ->
												exports.client.set(productObj.product.product_gold_key,productObj.product.tag)
												deferred.resolve productObj
								else if(!soldOut and productObj.isStyleMerging != "NO" and productObj.product_style == "New")
									console.log("productObj.isStyleMerging == YES")
									console.log(productObj.product_style)
									mysqlConnection.query 'INSERT INTO product_gold SET ?', productObj.product, (err1, result1) ->
										if err1
											console.log "addProduct - insert " + err1
											return deferred.resolve productObj
											# deferred.reject new Error(err1) + " -> Error addProduct - insert"	
										else
											productObj.product.id = result1.insertId
											productObj.product_already_exist = false
											exports.client.select 7, (err) ->
												exports.client.set(productObj.product.product_gold_key,productObj.product.tag)
												deferred.resolve productObj
								else
									console.log("Old product and productObj.isStyleMerging "+ productObj.isStyleMerging)
									productObj.product.id = 0
									productObj.product_already_exist = false
									deferred.resolve productObj
							else
								console.log("Alredy Exist")
								exports.client.select 4, (err) ->
									exports.client.hget productObj.product.product_gold_key,'id',(err, id) ->
										console.log(id)
										# Product exists; assign product id
										productObj.product.id = id
										productObj.product_already_exist = true
										deferred.resolve productObj
						else
							deferred.reject new Error(err.code) + " -> Error addProduct - select"
	return deferred.promise
			
	
#_______________________________________________________________________________
#	@desc get term ID; If enity type exist then get Entity ID, create it if create flag is true
#	@param Binding param @entityType as entity type such as size and color
#	@param Binding @mysqlConnection as mysql connection
#	@param Binding param @term 
#	@param Binding param @localeID 
#	@param Binding param @create ; if true then create the term or entity 
#	@return term ID, or entity ID

mapTerm = () ->
	deferred = exports.q.defer()
	console.log("mapTerm")
	# attach the term to an entity; if entityType = null then create the term without attaching it to an entity.
	entityType = @entityType
	term = @term
	# flag to create the term or just return term id if exist or null if not.
	if(isNaN(term))
		Terms_value=term.toLowerCase()
	else
		Terms_value=term
	if(isNaN(entityType))
		Type_value=entityType.toLowerCase()
	else
		Type_value=entityType
	console.log(term)
	console.log(Terms_value)
	console.log(entityType)
	console.log(Type_value)
	exports.client.select 3, (err) ->
		if !err
			exports.client.hexists Type_value,Terms_value, (err, reply) ->
				console.log(reply)
				if reply != 1
					# console.log(term)
					#The entity converts number to string.
					if(term.match(/^[\d\.\-]+$/i))
						entities=entityType+"="+'"' + term + '"'
					else	
						entities=entityType+"="+term
					deferred.resolve entities
				else
					exports.client.hget Type_value,Terms_value, (err, result) ->
						console.log(result)
						deferred.resolve entityType+"="+result
		else
			deferred.reject new Error(err.code) + " -> Error mapTerm " + sql 
		return	
	deferred.promise


#______________________________________________________________________________________________________________________
#	@desc Merge SKU History, by mapping color/size entities, replace the productObj SKU array by size/color entity IDs
#	@param Binding @mysqlConnection as mysql connection
#	@param Binding param @productObj as retailer object
#	@return productObj

#	Example
  		#skuHistory: 
			# { '0': [ '217273292', [ [ 'color', 'black' ], [ 'size', '6' ] ], [Object], '£65.00', '', 'true' ],
			#     '1': [ '217273307', [ [ 'color', 'blue' ], [ 'size', '6' ] ], [Object], '£65.00', '', 'true' ],
			# }

			# mapping entity type color named black by it's entity ID example 11
			# mapping entity type color named blue by it's entity ID example 12
			# mapping entity type size named 6 by it's entity ID example 13

  		#skuHistory: 
			# { '0': [ '217273292', [ 11, 13 ], [Object], '£65.00', '', 'true' ],
			#     '1': [ '217273307', [ 11, 13 ], [Object], '£65.00', '', 'true' ],
			# }

mergeSkuTerms = () ->

	#Create a promise
	deferred = exports.q.defer()
	# mysql connection from transact
	mysqlConnection = @mysqlConnection
	
	# product Object from addProduct
	productObj = @productObj
	console.log("mergeSkuTerms")
	# console.log JSON.stringify(productObj)
	# process.exit 0
	if (productObj.product_duplicate == false )
		# List of non repetitive entities from skuHistory
		skuEntities = []
		
		mappedSkuEntities = {}
		
		Object.keys(productObj.skuHistory).forEach (index) ->
			productObj.skuHistory[index][1].forEach (pair) ->
				if skuEntities.indexOf(pair.join(exports.splitter)) == -1
					if(productObj['translation'])
						if(productObj['translation'] == true)
							skuEntities.push(pair[0]+exports.splitter+pair[1])
						else
							skuEntities.push pair.join(exports.splitter)
					else
						skuEntities.push pair.join(exports.splitter)
					
		
		#skuEntities example
		# [ 'color¶black',
		#   'size¶6',
		#   'size¶8',
		#... ]
		console.log(skuEntities)
		mergeTerms = (index, doneCallback) ->
			entity = skuEntities[index].split(exports.splitter)
			exports.q()
			.then(mapTerm.bind(entityType:entity[0], term:entity[1]))
			.then(
				done =(termID) ->
					doneCallback null, termID
			)
		
		exports.async.mapSeries Object.keys(skuEntities), mergeTerms, (err, results) ->
			Object.keys(results).forEach (index) ->
				mappedSkuEntities[skuEntities[index]] = results[index]
				# console.log(skuEntities[index])
				# console.log(results[index])
				# console.log(mappedSkuEntities)

			#mappedSkuEntities example
			# [ 'color¶black': 4017,		# where 4017 is the entity id for entity type color named black
			#   'size¶6': 3961,
			#   'size¶8': 3953,
			#... ]

			# Map entity ID's back into productObj skuHistory
			Object.keys(productObj.skuHistory).forEach (index) ->
				if(productObj['translation'])
					if(productObj['translation'] == true)
						if(productObj['translation_type'])
							if(productObj['translation_type'] == "SDL")
								productObj.skuHistory[index]['raw_size']= productObj.skuHistory[index][1][1][1]
								productObj.skuHistory[index]['raw_color']= productObj.skuHistory[index][1][0][1]						
								skuGoldKey=generateUUID(productObj.product.product_gold_key + "_" + productObj.skuHistory[index][1][1][1].toString().toLowerCase().trim() + "_" + productObj.skuHistory[index][1][0][1].toString().toLowerCase().trim())
								productObj.skuHistory[index]['skuGoldKey']= skuGoldKey	
							else
								productObj.skuHistory[index]['raw_size']= productObj.skuHistory[index][1][1][2]
								productObj.skuHistory[index]['raw_color']= productObj.skuHistory[index][1][0][2]
								skuGoldKey=generateUUID(productObj.product.product_gold_key + "_" + productObj.skuHistory[index][1][1][2].toString().toLowerCase().trim() + "_" + productObj.skuHistory[index][1][0][2].toString().toLowerCase().trim())
								productObj.skuHistory[index]['skuGoldKey']= skuGoldKey									
						else
							productObj.skuHistory[index]['raw_size']= productObj.skuHistory[index][1][1][2]
							productObj.skuHistory[index]['raw_color']= productObj.skuHistory[index][1][0][2]
							skuGoldKey=generateUUID(productObj.product.product_gold_key + "_" + productObj.skuHistory[index][1][1][2].toString().toLowerCase().trim() + "_" + productObj.skuHistory[index][1][0][2].toString().toLowerCase().trim())
							productObj.skuHistory[index]['skuGoldKey']= skuGoldKey	
					else
						productObj.skuHistory[index]['raw_size']= productObj.skuHistory[index][1][1][1]
						productObj.skuHistory[index]['raw_color']= productObj.skuHistory[index][1][0][1]						
						skuGoldKey=generateUUID(productObj.product.product_gold_key + "_" + productObj.skuHistory[index][1][1][1].toString().toLowerCase().trim() + "_" + productObj.skuHistory[index][1][0][1].toString().toLowerCase().trim())
						productObj.skuHistory[index]['skuGoldKey']= skuGoldKey						
				else
					productObj.skuHistory[index]['raw_size']= productObj.skuHistory[index][1][1][1]
					productObj.skuHistory[index]['raw_color']= productObj.skuHistory[index][1][0][1]						
					skuGoldKey=generateUUID(productObj.product.product_gold_key + "_" + productObj.skuHistory[index][1][1][1].toString().toLowerCase().trim() + "_" + productObj.skuHistory[index][1][0][1].toString().toLowerCase().trim())
					productObj.skuHistory[index]['skuGoldKey']= skuGoldKey
				productObj.skuHistory[index][1].forEach (pair,i) ->
					if(productObj['translation'])
						if(productObj['translation'] == true)
							productObj.skuHistory[index][1][i] = mappedSkuEntities[pair[0]+exports.splitter+pair[1]]
						else
							productObj.skuHistory[index][1][i] = mappedSkuEntities[pair.join(exports.splitter)]
					else
						productObj.skuHistory[index][1][i] = mappedSkuEntities[pair.join(exports.splitter)]
			
			deferred.resolve productObj
			return
	else
		deferred.resolve productObj
		
	deferred.promise
#_______________________________________________________________________________
styleMerge = () ->
	console.log 'styleMerge'
	#Create a promise
	deferred = exports.q.defer()
	productObj = @productObj
	exports.client.select 4, (err) ->
		if productObj
			productObj.productReferenceNumber = productObj.product.product_gold_key
			if(isNaN(productObj.product.product_gold_key))
				if((productObj.product.product_gold_key).match(/^[\d\.]+$/i))
					productGoldKey=generateUUID(exports.retailer.retailer_code.toLowerCase().trim() + "_" + productObj.product.product_gold_key)
				else
					productGoldKey=generateUUID(exports.retailer.retailer_code.toLowerCase().trim() + "_" + (productObj.product.product_gold_key).toLowerCase().trim())
			else
				productGoldKey=generateUUID(exports.retailer.retailer_code.toLowerCase().trim() + "_" + productObj.product.product_gold_key)
			productObj.product.product_gold_key=productGoldKey
			name= productObj.product.name
			brand = productObj.product.brand
			if(isNaN(name))
				name=name.toLowerCase()
			if(isNaN(brand))
				brand=brand.toLowerCase()
			if productObj.isStyleMerging is 'Name'
					console.log("Name")
					exports.client.select 4, (err) ->
						exports.client.exists name, (err, reply) ->
							
							if(reply == 1)
								exports.client.get name, (err, result) ->
									console.log(result)
									productObj.product.product_gold_key = result
									productObj.product_style = "Old"
									deferred.resolve productObj
							else
								productObj.product_style = "New"
								deferred.resolve productObj
			else if productObj.isStyleMerging is 'Name and Brand'
				console.log("Name and Brand")
				syle_str=name+'_'+brand
				exports.client.select 4, (err) ->
					exports.client.exists syle_str, (err, reply) ->
						if(reply == 1)
							exports.client.get syle_str, (err, result) ->
								console.log(result)
								productObj.product.product_gold_key = result
								productObj.product_style = "Old"
								deferred.resolve productObj
						else
							productObj.product_style = "New"
							deferred.resolve productObj
			else 
				deferred.resolve productObj
	deferred.promise
	
referenceNumberMatch = () ->
	console.log 'referenceNumberMatch'
	#Create a promise
	deferred = exports.q.defer()
	productObj = @productObj
	new_gold_key=productObj.product.product_gold_key
	url=(productObj.product.product_url).toLowerCase()
	exports.client.select 4, (err) ->
		exports.client.exists url, (err, reply) ->
			if(reply == 1)
				exports.client.select 4, (err) ->
					exports.client.get url, (err, result) ->
						console.log("result=======>"+result)
						productObj.product.product_gold_key=result
						if(new_gold_key != result)
							write_string="New_gold_key : "+new_gold_key+"	Url : "+productObj.product.product_url+"	Old_gold_key : "+result
							exports.client.select 0, (err) ->
								exports.client.incr "ref_count"
								exports.fs.appendFile "/var/log/refno_mis_match.txt", write_string+"\n", (error) ->
									console.error("Error writing /var/log/refno_mis_match.txt file", error) if error
									deferred.resolve productObj
						else	
							deferred.resolve productObj
			else
				deferred.resolve productObj
				
	deferred.promise
#_______________________________________________________________________________
#	@desc add product
	#	Start Transact SQL
	#	addProduct add product in products table - If exist just update last_scrape_utc
	#	getCategoriesFacetsFromRedis	
	#	getCategoriesFacetsFromRedis return facets and categories from redis
	#	addProductTaxonomies perform these subtasks
	#	mapTaxonomiesTree function, return taxonomy ID
	#	insert into products_taxonomies product id, taxonomy id ) 
	#	addProductEntity to add prduct brand entity, create the brand entity if not exist.
	#	mergeSkuTerms Merge SKU History, by mapping color/size entities, replace the productObj SKU array by size/color entity IDs
	#	addSkuEntities add sku entry and entities_skus; update sku last_scrape_utc if exist
	#	addImages add image and images_skus entries
	#	addSkuHistory add products sku history to database; if sku history changed.
	#	commit the Transact; if there is an error rollback

#	@param productObj
#	@return

exports.addProductDetailsToDatabase = (productObj) ->
	deferred = exports.q.defer()
	if(productObj)
		if(productObj != 'done')
			exports.connectToMysql().then (mysqlConnection) ->
				mysqlConnection.beginTransaction (err) ->
					exports.q(productObj)
					.then(getCategoriesFacetsFromRedis.bind(productObj:productObj))
					.then(translationDetail.bind(productObj:productObj))
					.then(BrandLogic.bind(productObj:productObj))
					.then(styleMerge.bind(productObj:productObj))
					.then(referenceNumberMatch.bind(productObj:productObj))
					.then(addProduct.bind(mysqlConnection:mysqlConnection,productObj:productObj))
					.then(mergeSkuTerms.bind(mysqlConnection:mysqlConnection, productObj:productObj))
					.then(addSkuEntities.bind(mysqlConnection:mysqlConnection, productObj:productObj))
					.then(downloadImages.bind(mysqlConnection:mysqlConnection, productObj:productObj))
					.then(addSkuHistory.bind(mysqlConnection:mysqlConnection, productObj:productObj))
					.then(dele_md5_file.bind(productObj:productObj))
					.then(exports.detailLogger)
					.then(
						end = ()->
							console.log "commit " + productObj.product.product_url
							exports.detailLogger "commit " + productObj.product.product_url
							mysqlConnection.commit (err) ->
								if err
									mysqlConnection.rollback ->
										exports.detailLogger err
								mysqlConnection.end()
								deferred.resolve productObj
					)
					.fail((err) ->
						mysqlConnection.rollback ->
							exports.detailLogger err
						mysqlConnection.end()
						deferred.resolve productObj
					)

					console.log err
		else
			deferred.resolve null	
	else
		deferred.resolve null
	deferred.promise
# @producer: This gets information about product url which finish downloaded.
# Create jobs in redis for downloaded product url along with its md5 file and adds to queue.
# return status of the job 'completed' or 'failed'

exports.producer = () ->
	deferred = exports.q.defer()
	#Establishing redis connection
	# common_client1 = exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
	exports.common_client.on 'error', (err) ->
		deferred.resolve false
		console.log 'Error ' + err
		process.exit 0
		return
	exports.client.on 'error', (err) ->
		shared.errorLogger  'Error ' + err
		return
	#create channel name 
	subscriber_name=exports.retailer.retailer_group_name + ":" +exports.ip.address() 
	console.log(subscriber_name)
	#create channel for product url
	exports.common_client.SUBSCRIBE subscriber_name
	#Listen whether product url download been completed or not.
	# common_client1.SUBSCRIBE subscriber_name
	exports.common_client.on 'message', (channel, message) ->
		messageData=message.split("|")
		url=messageData[0]
		md5_file_name=messageData[1]
		job =exports.jobs.create(exports.retailer.retailer_code,
			title : url
			url : url
			md5_file_name : md5_file_name
			).save()
		job.on 'complete', ->
			console.log url + ' completed'
			exports.collectionCompletedLogger url + 'completed'
			exports.client.decr("job_count")
			exports.client.HSET("collection_completed",url,url)
			return
		job.on 'failed', ->
			console.log url + ' failed'
			exports.collectionCompletedLogger url + 'failed'
			exports.client.decr("job_count")
			# exports.client.HSET("collection_completed",url,url)
			return
		return
	# exports.common_client.unsubscribe()
	deferred.promise
	
# URL's fetched from queue and it is processed via scrapeTheProducts in sequential
# returns callback
exports.consumer = (retailer_code,retailerScript) ->
	sleep_time=Math.random()* (100000 - 10000) + 10000
	console.log("sleep_time==>"+sleep_time)
	setTimeout (->
		exports.jobs.process retailer_code,1,(job, done) ->
			URL = []
			URL.push job.data.url
			exports.common_client.on 'error', (err) ->
				console.log 'Error ' + err
				return
			exports.client.on 'error', (err) ->
				console.log 'Error ' + err
				return
			exports.translation_client.on 'error', (err) ->
				console.log 'Error ' + err
				return
			# exports.common_client.unsubscribe()
			# exports.client.unsubscribe()
			# exports.translation_client.unsubscribe()
			retailerScript.scrapeTheProducts(URL,job.data.md5_file_name,done)
			return
	),sleep_time
#_______________________________________________________________________________________________
#	@desc add sku entry and entities_skus; update sku last_scrape_utc if exist
#	@param Binding @mysqlConnection as mysql connection
#	@param Binding param @productObj as retailer object
#	@return productObj
addSkuEntities = () ->

	#Create a promise
	deferred = exports.q.defer()
	# mysql connection from transact
	mysqlConnection = @mysqlConnection

	# product Object from addProduct
	productObj = @productObj
	console.log("addSkuEntities")
	# console.log(productObj.skuHistory)
	if (productObj.product_duplicate == false )
		product_already_exist=productObj.product_already_exist
		addSkuEntity = (index, doneCallback) ->
		  # skuHistory: 
		  #  { '0': [ vendor_SKU,  [ size_entity_id, color_entity_id ], [Images], price_now, price_was, inStock ],
		  # .... }

			# entitiesIDs is array of size and color entities [ size_entity_id, color_entity_id ]
			entitiesIDs = productObj.skuHistory[index][1]
			entities=entitiesIDs[0]+"|"+entitiesIDs[1]
			skuGoldKey=productObj.skuHistory[index]['skuGoldKey']
			image=productObj.skuHistory[index][2].large
			md5file = crypto.createHash('md5').update(image).digest('hex').toUpperCase()
			imagefilename=md5file+'.jpg'
			stock=productObj.skuHistory[index][5]
			raw_color=productObj.skuHistory[index]['raw_color']
			raw_size=productObj.skuHistory[index]['raw_size']
			# Do we have SKU ID
			exports.client.select 6, (err) ->
				console.log("skuGoldKey===> "+skuGoldKey)
				exports.client.hexists skuGoldKey,'id', (err, reply) ->
					console.log("reply11===> "+reply)
					if !err
						if reply == 0
							console.log("reply22===> "+reply)
							priceWas = productObj.skuHistory[index][4]
							priceNow = productObj.skuHistory[index][3]
							# console.log JSON.stringify(productObj)
							# process.exit 0
							# console.log(priceNow)
							if priceWas.length > 0
								originalPrice = Number(priceWas.replace(/[^0-9\.]+/g, ''))
								originalPriceUtc = exports.reportingYesterdayDate
							else if priceNow.length > 0
								originalPrice = Number(priceNow.replace(/[^0-9\.]+/g, ''))
								originalPriceUtc = exports.reportingDate
							else
								originalPrice = null
								originalPriceUtc = exports.reportingYesterdayDate
							
							SKU = 
								sku_gold_key : skuGoldKey
								product_gold_key : productObj.product.product_gold_key
								original_price : originalPrice
								image_filename : imagefilename
								entities : entities
								raw_color : raw_color
								raw_size : raw_size
							# console.log(SKU)
							if(product_already_exist == false)
								if(stock == true)
									mysqlConnection.query 'INSERT INTO sku_gold SET ?', SKU, (err, result) ->
										if !err
											doneCallback null, null
										else
											# deferred.reject new Error(err) + " -> Error addSkuEntities - insert"
											console.log "Error addSkuEntities - insert" + err
											doneCallback null, null
								else
									doneCallback null, null
							else 	
								mysqlConnection.query 'INSERT INTO sku_gold SET ?', SKU, (err, result) ->
									if !err
										doneCallback null, null	
									else
										console.log "Error addSkuEntities - insert" + err
										doneCallback null, null
										# deferred.reject new Error(err) + " -> Error addSkuEntities - insert"
						else
							doneCallback null, null
					else
						deferred.reject new Error(err.code) + " -> Error mergeSkuRow " + sql

		exports.async.map Object.keys(productObj.skuHistory), addSkuEntity, (err, results) ->
			deferred.resolve null
	else
		deferred.resolve productObj
		
	deferred.promise
#___________________________________________________________________________________________
#	downloadImages productObj
#	generates image file name for the input image url, check for the existence and file size 
#   download the image if the not exists or file size is 0
#	@return productObj
downloadImages = () ->
	deferred = exports.q.defer()
	productObj = @productObj
	mysqlConnection = @mysqlConnection
	images_array=[]
	console.log("downloadImages")
	images_array= Object.keys(productObj.skuHistory)
	if(productObj['default_image'])
		images_array.push productObj['default_image']
	# common_client = exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
	exports.common_client.on 'error', (err) ->
		console.log 'Error ' + err
		return
	#Check for Duplicate products 	
	if (productObj.product_duplicate == false )
		downloadImage = (index, doneCallback) ->
			if(isNaN(index))
				image=index
			else
				image=productObj.skuHistory[index][2].large
			console.log(image)
			md5file = crypto.createHash('md5').update(image).digest('hex').toUpperCase()
			imagefilename=md5file+'.jpg'
			imagefilename_grid=md5file+'.grid.jpg'
			firstLevel=md5file.substring(0,1)
			secondLevel=md5file.substring(1,2)
			thirdLevel=md5file.substring(2,3)
			
			filepath="#{imagePath}/#{exports.retailer.retailer_code}/#{firstLevel}/#{secondLevel}/#{thirdLevel}/#{imagefilename}"
			gridfilepath="#{imagePath}/#{exports.retailer.retailer_code}/#{firstLevel}/#{secondLevel}/#{thirdLevel}/#{imagefilename_grid}"
			if(imageHash.get(md5file))
				console.log("Images already downloaded for this product...")
				doneCallback null, null
			else
				fileSize=0
				imageHash.set(md5file,md5file)
				stats = fs.existsSync(filepath)
				gridstats = fs.existsSync(gridfilepath)
				if(gridstats == true)
					stat = fs.statSync(gridfilepath)
					fileSize = stat["size"]
				else if(stats == true)
					stat = fs.statSync(filepath)
					fileSize = stat["size"]
				if(fileSize <= 0)
					machine_detail={}
					machine_detail['IP']=exports.ip.address()+":"+exports.process.pid
					machine_detail['retailer_group_name']=exports.retailer.retailer_group_name
					machine_detail['Type']="image"
					machine_detail['URL']="image"
					machine_detail['Lable']="image"
					machine_detail['filepath']=filepath
					exports.auth['method']='GET'
					exports.auth['url']=image
					exports.auth['proxy']=exports.retailer.proxy_detail
					auth_string=JSON.stringify(exports.auth)
					machine_detail_string=JSON.stringify(machine_detail)
					push_string=auth_string + exports.splitter + machine_detail_string
					common_client1=exports.redis.createClient(exports.common_redisConfig.port, exports.common_redisConfig.IP)
					common_client1.select 1, (err) ->
						#Image urls push into common redis
						common_client1.rpush exports.retailer.retailer_code, push_string
						console.log("Default Image downloaded completed- #{imagefilename}")
						common_client1.quit()
						return doneCallback null, null
						
					
				else
					console.log("Image Already available - #{imagefilename}")
					# exports.common_client.unsubscribe()
					doneCallback null, null	
		exports.async.map images_array, downloadImage, (err, results) ->
			deferred.resolve null		
	else
		# exports.common_client.unsubscribe()
		deferred.resolve productObj
		
	deferred.promise
	
##_______________________________________________________________________________

exports.romanize = (num) ->
  lookup = 
    M: 1000
    CM: 900
    D: 500
    CD: 400
    C: 100
    XC: 90
    L: 50
    XL: 40
    X: 10
    IX: 9
    V: 5
    IV: 4
    I: 1
  roman = ''
  i = undefined
  for i of lookup
    `i = i`
    while num >= lookup[i]
      roman += i
      num -= lookup[i]
  roman

