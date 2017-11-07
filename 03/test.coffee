#'use strict'
request = require("request")
cheerio = require("cheerio")
async = require("async")
Q=require("q")
fs = require('fs')
json2xls = require('json2xls')

form_url_with_headers = (url) ->
	deferred=Q.defer()
	if url!= ""
		options =
			url:url,
			method:"GET",
			header:
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
				'Content-Type':'application/x-www-form-urlencoded'
		deferred.resolve options
	else
		console.log "error"
		deferred.reject "No url Passed"
	return deferred.promise

exports.process_1 = (first_level_url) ->
	deferred=Q.defer()
	url_list=[]
	console.log first_level_url
	form_url_with_headers(first_level_url).then((first_url) ->
		console.log first_url
		req first_url,(response,content) ->
		fs.writeFileSync 'first_level.html' , content.toString() , 'binary'
		$=cheerio.load(content)
		links=$("#nav .level0.nav-7.level-top.parent a").attr("href")
		url_list.push(links)
	deferred.resolve first_level_url
return deferred.promise