configs =  dict()
configs["model1"] = {"name":"qwen/qwen3-32b",
                     "temperature":0.6,
                     "provider":"groq",
                     "limits":{"requests_per_minute":60,
                               "requests_per_day":1000,
                               "tokens_per_minute":6000,
                               "tokens_per_day":500_000}}