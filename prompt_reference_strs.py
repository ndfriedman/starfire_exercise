#written by Noah Friedman
#Returns specific reference data to the llm (e.g. database config)

jsonObj = {"medicare_data_api_links": {
    # Medicare Part D Prescribers — by Geography and Drug
    "medicare-part-d-prescribers-by-geography-and-drug": {
        "2021": "7dda2a9d-034a-446a-b4b3-e1254e0127b2",  
        "2022": "1fc57194-a51d-4864-aee6-de0889488151",  
        "2023": "c8ea3f8e-3a09-4fea-86f2-8902fb4b0920"  
    },  

    # Medicare Part D Prescribers — by Provider (NPI)
    "medicare-part-d-prescribers-by-provider": {
        "2021": "3f7ab9ce-6fb6-4e6b-9af3-b681f2d3a95e", 
        "2022": "bed99012-c527-4d9d-92ea-67ec2510abea", 
        "2023": "14d8e8a9-7e9b-4370-a044-bf97c46b4b44"  
    },  

    # Medicare Part D Prescribers — by Provider and Drug (NPI + Drug)
    "medicare-part-d-prescribers-by-provider-and-drug": {
        "2021": "7dda2a9d-034a-446a-b4b3-e1254e0127b2",  
        "2022": "1fc57194-a51d-4864-aee6-de0889488151", 
        "2023": "c8ea3f8e-3a09-4fea-86f2-8902fb4b0920" 
    }

    },

    "dataset_description": (
    	"The dataset you are working with is the database of medicare part d providers.\n"
		"This data captures medicare-part-d-prescribers-by-geography-and-drug, medicare-part-d-prescribers-by-provider, and medicare-part-d-prescribers-by-provider-and-drug for the years between 2021-2023"
    	)   
}


def get_val(key):
	return jsonObj[key]


