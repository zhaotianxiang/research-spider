# rocketreach 批量获取数据

## 1. 人员数据结构(不需要花费点数)

```json
{
    "_id": ObjectId("62a568435234eaf26988f560"),
    "id": "50640461",
    "birth_year": "1986",
    "city": "",
    "country_code": "KR",
    "current_employer": "KBS (Korean Broadcasting System)",
    "current_title": "Comedian",
    "gender": "male",
    "linkedin_url": "https://www.linkedin.com/in/şinasi-alpago-80345a89",
    "links": "",
    "location": "South Korea",
    "name": "Şinasi Alpago",
    "normalized_title": "Comedian",
    "profile_pic": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQNsh0aiN34v66XhLlvoCeYkdRZ7lrvS1DkUgtN2MFnofHYTtGw5okQjOo",
    "region": "",
    "status": "not queued",
    "teaser": "{'emails': [], 'phones': [], 'preview': ['kbs.co.kr', 'gmail.com'], 'is_premium_phone_available': False}"
}
```

## 2. 人员详细数据(花费点数)

```json
{
    "profile_list": {
        "id": 11907775,
        "name": "API Contacts"
    },
    "id": 5244,
    "status": "complete",
    "name": "Marc Benioff",
    "profile_pic": "https://d1hbpr09pwz0sk.cloudfront.net/profile_pic/marc-benioff-4492e698",
    "linkedin_url": "https://www.linkedin.com/in/marcbenioff",
    "links": {
        "linkedin": "https://www.linkedin.com/in/marcbenioff",
        "twitter": "https://twitter.com/benioff",
        "angellist": "https://angel.co/benioff",
        "quora": "https://quora.com/marc-benioff",
        "facebook": "https://facebook.com/benioff",
        "pinterest": "https://pinterest.com/benioff",
        "instagram": "https://instagram.com/benioff",
        "klout": "https://klout.com/benioff",
        "aboutme": "https://about.me/marcbenioff",
        "gravatar": "https://gravatar.com/crmmaster",
        "google+": "https://plus.google.com/108172009599607363531/about",
        "hi5": "https://www.hi5.com/friend/p45336146--profile--html",
        "amazon": "https://www.amazon.com/gp/pdp/profile/AZGYQG724J6ON//190-5748375-2756131",
        "twicsy": "https://twicsy.com/u/%40Benioff",
        "salesforce.com": "https://www.salesforce.com/company/leadership/executive-team/index.jsp#benioff",
        "gravatar.com": "https://gravatar.com/crmmaster"
    },
    "location": "San Francisco, CA, US",
    "current_title": "Chair & CEO",
    "normalized_title": "Chair Springer",
    "current_employer": "salesforce.com",
    "current_work_email": "marc_benioff@salesforce.com",
    "current_personal_email": "benioff@aol.com",
    "emails": [
        {
            "email": "benioff@gmail.com",
            "smtp_valid": "valid",
            "type": "personal"
        },
        {
            "email": "benioff@aol.com",
            "smtp_valid": "valid",
            "type": "personal"
        },
        {
            "email": "mbenioff@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "marcb@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "marc@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "ceo@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "marc.benioff@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "marc_benioff@salesforce.com",
            "smtp_valid": "valid",
            "type": "professional"
        },
        {
            "email": "benioff@frontiernet.net",
            "smtp_valid": "valid",
            "type": "personal"
        },
        {
            "email": "benioff@comcast.net",
            "smtp_valid": "valid",
            "type": "personal"
        },
        {
            "email": "cooldwj@chinaren.com",
            "smtp_valid": "invalid",
            "type": "professional"
        },
        {
            "email": "benioff@rcn.com",
            "smtp_valid": "invalid",
            "type": "professional"
        }
    ],
    "phones": [
        {
            "number": "773-444-9010",
            "type": "mobile"
        },
        {
            "number": "415-706-8145",
            "type": "mobile"
        },
        {
            "number": "415-901-7000",
            "type": "professional"
        },
        {
            "number": "415-901-7040",
            "type": "fax"
        },
        {
            "number": "415-901-7006",
            "type": null
        },
        {
            "number": "650-434-4319",
            "type": null
        },
        {
            "number": "415-901-7008",
            "type": null
        },
        {
            "number": "415-434-4319",
            "type": null
        },
        {
            "number": "415-260-0008",
            "type": "mobile"
        },
        {
            "number": "808-882-7587",
            "type": null
        }
    ],
    "job_history": [
        {
            "is_current": true,
            "title": "Chair & CEO",
            "company": "salesforce.com",
            "company_name": "salesforce.com",
            "end_date": "Present",
            "start_date": "1999-02-28",
            "last_updated": "2022-06-09 01:44:20.748298",
            "description": ""
        },
        {
            "is_current": false,
            "title": "Senior Vice President",
            "company": "Oracle Corporation",
            "company_name": "Oracle Corporation",
            "end_date": "1999-06-01",
            "start_date": "1986-04-30",
            "last_updated": "2022-06-09 01:44:20.748298",
            "description": ""
        }
    ],
    "education": [
        {
            "start": 1982,
            "end": 1986,
            "degree": "Bachelor of Science in Business Administration",
            "major": "Entrepreneurship",
            "school": "University of Southern California"
        }
    ],
    "recommended_email": "marc_benioff@salesforce.com",
    "recommended_personal_email": "benioff@aol.com",
    "recommended_professional_email": "marc_benioff@salesforce.com",
    "skills": [],
    "birth_year": 1964,
    "gender": "male"
}
```

3. 公司详细数据

```json
{
    "id": 18097967,
    "name": "Rocketreach.co",
    "domain": "rocketreach.co",
    "email_domain": "rocketreach.co",
    "website_domain": "rocketreach.co",
    "ticker_symbol": null,
    "links": {
        "twitter": null,
        "facebook": null,
        "linkedin": "http://linkedin.com/company/rocketreach.co",
        "crunchbase": null
    },
    "year_founded": 2015,
    "address": {
        "description": "800 Bellevue Way NE Suite 500, Bellevue, Washington 98004, US",
        "street": "800 Bellevue Way NE Suite 500",
        "city": "Bellevue",
        "region": "Washington",
        "postal_code": "98004",
        "country_code": "US"
    },
    "phone": "(833) 212-3828",
    "fax": null,
    "num_employees": 81,
    "revenue": 30000000,
    "funding_investors": null,
    "industry": "Information Services",
    "sic_codes": [
        73,
        737
    ],
    "rr_profile_url": "https://rocketreach.co/rocketreachco-profile_b4d23efdf855f2de",
    "description": "4 Million+ businesses worldwide trust RocketReach. Including the biggest - Google, Amazon, Apple, Facebook, and 90% of S&P 500. Access real-time verified personal/professional emails, phone numbers, social media links for over 400 million profiles, at 10 million companies worldwide."
}
```
