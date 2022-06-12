# rocketreach 

```
        item = {
            'reporter_id': reporter_id,
            '人员编号': id,
            '人员名称': name,
            '地区': region,
            '城市': city,
            '城市代码': country_code,
            '雇主信息': current_employer,
            '当前职位': current_title,
            '当前领英地址': linkedin_url,
            '地理位置': location,
            '正式职位': normalized_title,
            '人员状态': status,
            '附加信息': other,
            '头像信息（源数据）': profile['profile_pic'],
            '社交账号（源数据）': profile['links'],
            '工作经历（源数据）': profile['job_history'],
            '教育经历（源数据）': profile['education'],
            '邮箱地址（源数据）': profile['emails'],
            '电话号码（源数据）': profile['phones']
        }
        # profile info
        self.logger.info("people : %s \n\n", people)
        # added
        if profile['emails'] is not None:
            item['邮箱列表'] = "\n".join(list(map(lambda e: e['email'], profile['emails'])))
        if profile['phones'] is not None:
            item['电话列表'] = "\n".join(list(map(lambda p: p['number'], profile['phones'])))
        if profile['job_history'] is not None:
            item['工作列表'] = "\n".join(list(map(parse_job_history, profile['job_history'])))
        if profile['education'] is not None:
            item['教育列表'] = "\n".join(list(map(parse_education, profile['education'])))
        if profile['links'] is not None:
            for link in profile['links']:
                print("link", link)
                item[link] = profile['links'][link]
        item['最原始详情数据'] = profile
```

## 1. reporter 表
  - 