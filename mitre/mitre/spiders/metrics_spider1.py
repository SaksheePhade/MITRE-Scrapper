import scrapy, time
import re
import string, collections
from ..items import MitreItem
#import logging
#from scrapy.utils.log import configure_logging 

class MetricsSpider(scrapy.Spider):
	name = 'metrics'  #name of the spider
	start_urls = [
		'https://attack.mitre.org'
	]

	def parse(self, response):
		url = response.css('table.techniques-table a::attr(href)').extract()
		for item in url:
			time.sleep(0.2)
			yield response.follow(item, callback = self.parse_dir_contents)

	def parse_dir_contents(self, response):
		TechniqueData = {}
		techniquename = response.css('h1::text').extract()
		techniquename = "".join(techniquename).strip().replace("\n", "")
		TechniqueData['techniquename'] = techniquename

		TechniqueData['detection'] = "".join(response.xpath("//div[@class = 'container-fluid']/div/p/text()").extract())
		TechniqueData['description'] = "".join(response.xpath("//div[@class = 'description-body']/p/a/text()" + "|" 
			+ "//div[@class = 'description-body']/p/text()").extract())	

		Mitigations = {}
		ProcedureExamples = {}		    

		tables = response.xpath("//table[@class = 'table table-bordered table-alternate mt-2']")

		for i in range(len(tables)):
			type = tables[i].xpath('thead/tr/th/text()').extract()[1]
			for row in tables[i].xpath('tbody/tr'):
				keys = row.xpath('td/a/text()')[0].extract() 
				mid_values = row.xpath('td/a/text()')[1].extract()
				values = row.xpath("td/p/text()" + "|" + "td/p/a/text()").extract()
				values = "".join(values)
				keys=''.join(e for e in keys if e.isalnum())
				keys=re.sub(" ","",keys)
				keys=re.sub("-","",keys)
				if type == "Name":
					ProcedureExamples[keys.strip()] = mid_values + " : " + values
				elif type == "Mitigation":
					Mitigations[keys.strip()] = mid_values + " : " + values

		if Mitigations:
			TechniqueData['mitigations'] = Mitigations
		if ProcedureExamples:
			TechniqueData['procedureexamples'] = ProcedureExamples
			if not Mitigations:
				Mitigations['mitigations'] = response.xpath("//div[@class = 'container-fluid']/p[not(@scite-citeref-number)]/text()").extract()[0].strip() 
				TechniqueData['mitigations']= Mitigations

		keys = response.xpath("//span[@class = 'h5 card-title']")
		values = response.xpath("//div[@class = 'col-md-11 pl-0']")
		datasource_val={}
		data_value=""

		for i in range(len(keys)):
			key = keys[i].xpath('text()').extract()
			key[0] = key[0].replace("\xa0", "")
			key[0] = re.sub("\s","",key[0])
			key[0] = re.sub("-","",key[0])
			key[0] = re.sub(":","",key[0])
			key[0] = key[0].lower()
			value = values[i].xpath('text()' + "|" + "a/text()").extract()
			
			if key[0]=="datasources":
				key_value = values[i].xpath("a/text()").extract()
				ds_url = values[i].xpath("a/@href").extract()
				data_value=values[i].xpath("text()").extract()
				
				for i in range(len(data_value)):
					data_value[i] = data_value[i].strip()
					data_value[i] = data_value[i].replace(":", "")
					data_value[i] = data_value[i].replace(",", "")
					if ("\n" in data_value[i]) :
						data_value.remove(data_value[i])
				while("" in data_value) :
					data_value.remove("")
				for i in range(len(data_value)):
					data_value[i] = data_value[i].strip().lower()
				
				temp_val={}
				for k, v, vi in zip(key_value, ds_url, data_value):
					k = k.strip()
					if k in temp_val:
						temp_val[k].append(vi)
					else:
						temp_val[k] = [v, vi]
				datasource_val = temp_val


			elif key[0]=="id" or key[0]=="subtechniqueof" or key[0]=="created" or key[0]=="lastmodified" or key[0]=="version":
				temp_val=""
				for j in range(len(value)):			
					value[j] = value[j].strip()
					if not "\n" in value[j] and len(value[j]) > 1:
						temp_val+=value[j]
			else:
				temp_val = []
				for j in range(len(value)):	
					value[j] = value[j].strip()
					if not "\n" in value[j] and len(value[j]) > 1:
						temp_val.append(value[j])
						
			if key[0] == "tactic":
				TechniqueData["tactics"] = temp_val
				
			elif key[0] == "id":
				TechniqueData["tid"] = temp_val
			else :
				TechniqueData[key[0].lower()] = temp_val
        
		if len(datasource_val) > 0:
			res1 = list(datasource_val.keys())[0]
			res = datasource_val[res1]
			yield scrapy.Request(res[0], callback=self.parse_ds_contents, meta={'ds': res[1:], 'MainDict':TechniqueData, 'spc' : 1}, dont_filter=True)

		else:
			yield MitreItem(**TechniqueData)	
		
	#function for scraping datasources
	def parse_ds_contents(self, response):
		item = response.meta.get('ds')
		MainDict=response.meta.get('MainDict')
		
		ds = {}
		rs = {}
		xyz = collections.defaultdict(dict)
		rel = []
		git_name = response.xpath("//span[@class = 'pl-s']/text()").extract_first()
		rows = response.css('.js-file-line-container tr')
		for row, i in zip(rows, range(len(rows))):
			tds = row.css('td')[1]
			key = tds.css('.pl-ent::text').extract()
			value = tds.css('.pl-s::text').extract()
			if key and ((key[0] == 'name' and i != 0) or key[0] == 'type' or key[0] == 'description'):
				if key[0] == "name" and rel:
					if ds["name"].lower() in item:
						xyz[ds["name"]]["name"] = ds["name"]
						xyz[ds["name"]]["type"] = ds["Type"]
						xyz[ds["name"]]["description"] = ds["description"]
						xyz[ds["name"]]["relationships"] = []
						for i in range(len(rel)):
							tm = {}
							tm["source_data_element"] = rel[i]["source_data_element"]
							tm["relationship"] = rel[i]["relationship"]
							tm["target_data_element"] = rel[i]["target_data_element"]
							xyz[ds["name"]]["relationships"].append(tm)

					rel.clear()
					ds[key[0]] = value[0]
				elif key[0] == 'type' :
					ds[key[0].capitalize()] = value[0]
				else:
					ds[key[0]] = value[0]
				
			if key and (key[0] == 'source_data_element' or key[0] == 'relationship'):
				rs[key[0]] = value[0]
			if (key and key[0] == 'target_data_element'):
				if value:
					rs[key[0]] = value[0]
				else:
					rs[key[0]] = ""
				rel.append(dict(rs))
				ds['relationships'] = rel

		if ds and (ds["name"].lower() in item):
			xyz[ds["name"]]["name"] = ds["name"]
			xyz[ds["name"]]["type"] = ds["Type"]
			xyz[ds["name"]]["description"] = ds["description"]
			xyz[ds["name"]]["relationships"] = []
			for i in range(len(rel)):
				tm = {}
				tm["source_data_element"] = rel[i]["source_data_element"]
				tm["relationship"] = rel[i]["relationship"]
				tm["target_data_element"] = rel[i]["target_data_element"]
				xyz[ds["name"]]["relationships"].append(tm)

		for kyz in xyz:
			MainDict['datasources'][git_name].append(xyz[kyz])

		spc = response.meta.get('spc')
		if(spc == len(MainDict['datasources'])):
			for kks in MainDict['datasources']:
				list1 = MainDict['datasources'][kks]
				list2 = []
				for li in list1:
					if type(li) is dict:
						list2.append(li)
				MainDict['datasources'][kks] = list2
			yield MitreItem(**MainDict)

		else:
			ks =  list(MainDict['datasources'].keys())[spc]
			uu = MainDict['datasources'][ks]
			time.sleep(0.5)
			yield scrapy.Request(uu[0], callback=self.parse_ds_contents, meta={'ds': uu[1:], 'MainDict':MainDict, 'spc' : spc + 1}, dont_filter=True)