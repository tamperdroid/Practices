exports = module.exports = {}

try
	shared = require('/opt/goldrush-worker/shared')
	HashMap = require('hashmap')
	spawn   = require("child_process").spawn
	# shared = require('./shared')
catch e
	console.error e.message, if e.code == 'MODULE_NOT_FOUND' then 'please install it (npm install module_name)' else ''
	process.exit e.code
	
proxy=""	
totalHash = new HashMap()
exports.retailer_group_detail=""
retailer_group_name=process.argv[2].toString()
hits_per_second=process.argv[3]
# shared.mysqlConfig['database'] =  "scraper_"+retailerCode.replace("-","")
# shared.mysqlConfig['database'] =  "davidlawrence_ginger"
proxy=process.argv[4]
retailer_name_list=[]
interval_time=1000
if(hits_per_second % 1 != 0)
	result_values=1/hits_per_second
	console.log hits_per_second
	console.log result_values
	# if(result_values % 1 != 0)
		# result_values=Number((result_values.toFixed()))+1
		# console.log result_values
	interval_time=Number(result_values)*1000
console.log interval_time
status={}
server_ip_client = shared.redis.createClient(shared.server_ip_client_redisConfig.port, shared.server_ip_client_redisConfig.IP)
shared.client.on 'error', (err) ->
	shared.errorLogger  'Error ' + err
	return
#queuing : This fetch url from common redis and download content 
#store the content with respective md5 file name in common redis
#Then publish the message to respective channel
queuing = ->
	deferred = shared.q.defer()
	# Establishing redis 
	# client = shared.redis.createClient(shared.redisConfig.port, shared.redisConfig.IP)
	# console.log(shared.retailer_group_data)
	#calculation for hits/sec
	retalercount = ->
		total_retailers=(shared.retailer_group_data).length
		if(total_retailers != 0)
			clearInterval(intervalId_retalercount)
			if(hits_per_second % 1 != 0)
				list=[1]
			else
				hits_per_second_per_retailer=(hits_per_second/total_retailers).toFixed()
				list=[1..hits_per_second_per_retailer]
			console.log list
			# @retrieveResponse: This executes for every 1 sec. 
			retrieveResponse = ->
				#iterating each retailer from retailer group.
				shared.retailer_group_data.forEach (retailer) ->
					retailer_name=retailer.toString()
					#Loop for executing which is based on hit/sec 
					list.forEach (count) ->
						#Change DB
						shared.client.select 1, (err) ->
							#To check the retailer list whether it exists or not.
							shared.client.exists retailer_name , (err, reply) ->
								if(reply == 1)
									status[retailer_name]=true
									#fetch url from list
									shared.client.rpop retailer_name, (err, result) ->
										if(result)
											# console.log("result==>"+result)
											datas=result.split(shared.splitter)
											shared.auth=JSON.parse(datas[0])
											machine_detail=JSON.parse(datas[1])
											url=shared.auth['url']
											if(shared.auth['method'] == 'POST')
												url_md5=machine_detail['md5']
											else
												url_md5=shared.crypto.createHash('md5').update(url).digest('hex').toUpperCase()
											delete(shared.auth['url'])
											delete(shared.auth['encoding'])
											if(Object.keys(retailer_name_list).length > 0)
												SuperProxy=retailer_name_list[retailer_name]
												shared.auth['proxy']=SuperProxy
											if(machine_detail['Lable'] == "image")
												delete shared.auth['headers']['Accept-Encoding']
												delete shared.auth['headers']['Content_Type']
												delete shared.auth['json']
												shared.auth['encoding']='binary' 
											#Download the content 
											if(totalHash.get(url_md5))
												if(machine_detail['Lable'] != "image" or machine_detail['URL'] != 'SKU')
													message=url+"|"+url_md5
													publish_string=machine_detail['retailer_group_name']+":"+machine_detail['IP']
													shared.client.PUBLISH(publish_string,message)
											else
												if(machine_detail['Script'] == "perl")
													post_content=""
													console.log("url==>"+url)
													# perl_path="/home/merit/Merit_Robots/"+retailer_name+"-detail.pl"
													perl_path="/opt/goldrush-worker/robots/"+retailer_name+"-detail.pl"
													console.log("perl_path==>"+perl_path)
													#process2 = spawn('perl',["/opt/goldrush-worker/robots/"+retailer_name+"-detail.pl",url,url_md5,post_content])
													process2 = spawn('perl',[perl_path,url,url_md5,post_content])
													if(machine_detail['URL'] != 'SKU')
														setTimeout (->
															message=url+"|"+url_md5
															publish_string=machine_detail['retailer_group_name']+":"+machine_detail['IP']
															shared.client.PUBLISH(publish_string,message)
														),2000
												else
													shared.download url,0,machine_detail['Lable'], (Data) ->
														if Data
															totalHash.set(url_md5,url_md5)
															if(machine_detail['Lable'] == "image")
																shared.fs.writeFile machine_detail['filepath'], Data, 'binary', (error) ->
																	if error
																		console.log(error)
																		shared.errorLogger("Error writing file", error)
															else
																if(typeof(Data) == 'object')
																	Data=JSON.stringify(Data)
																else if(machine_detail['Type'] == "JSON")
																	Data=JSON.stringify(Data)
																
																# url_md5=shared.crypto.createHash('md5').update(url).digest('hex').toUpperCase()
																message=url+"|"+url_md5
																publish_string=machine_detail['retailer_group_name']+":"+machine_detail['IP']
																# publish_string="kohls:172.20.240.194"
																#Change DB
																shared.client.select 2, (err) ->
																	#To store content in redis
																	shared.client.set(url_md5,Data)
																	#Publish message 
																	if(machine_detail['URL'] != 'SKU')
																		# console.log(publish_string)
																		# console.log(message)
																		shared.client.PUBLISH(publish_string,message)
														else
															console.log("url_md5"+url_md5)
															shared.client.set(url_md5,"ERR")
										else
											console.log("Else"+result)
										
									return
								else if(status[retailer_name])
									console.log(retailer_name+"==>completed")
							return
						return
					return
					
			intervalId = setInterval(retrieveResponse, interval_time)	
		return
	intervalId_retalercount = setInterval(retalercount, interval_time)
	deferred.promise
	
lumSuperProxy = ->
	deferred = shared.q.defer()
	console.log("lumSuperProxy")
	setTimeout (->
		SuperProxy = (retailer, doneCallback) ->
			retailer_name=retailer.toString()
			console.log(retailer_name)
			shared.auth['method']='GET'
			shared.auth['json']=true
			shared.auth['proxy']=''
			shared.auth['headers']['Content_Type']='application/x-www-form-urlencoded'
			shared.auth['headers']['User-Agent']='Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'
			ip_Response = ->
				server_ip_client.select 5, (err) ->
					server_ip_client.get retailer_name+"::proxy", (err, luminatiSuperProxy) ->
						console.log(luminatiSuperProxy)
						if((luminatiSuperProxy.match(/http/i)) or !(luminatiSuperProxy.match(/lum/i)))
							clearInterval(ip_intervalId)
						if(luminatiSuperProxy.match(/lum/i))
							shared.download shared.luminatiSuperProxy, 0,"detail", (SProxy) ->
								setTimeout (->
									SProxy=luminatiSuperProxy.replace(/superproxy/ig,SProxy)
									retailer_name_list[retailer_name]=SProxy
									doneCallback(null, null)
								),2000
						else
							doneCallback(null, null)
			ip_intervalId = setInterval(ip_Response, 300000)
		console.log(shared.retailer_group_data)
		shared.async.mapSeries shared.retailer_group_data, SuperProxy, (err, results) ->
			deferred.resolve null
			return
	),2000
	deferred.promise
	
#To check retailer group name null or not and then call the queuing functions 
controleorfun = ->
	deferred = shared.q.defer()
	shared.q(retailer_group_name)
	.then(shared.get_retailergroup_ips(retailer_group_name))
	.then(lumSuperProxy)
	.then(queuing)
	.fail((err) ->
		shared.detailLogger "*" , err
	).end

	deferred.promise
if(retailer_group_name != "")
	shared.isRedisServeraLive()
	.then(controleorfun)
	.fail((err) ->
		shared.detailLogger "*" , err
	).end