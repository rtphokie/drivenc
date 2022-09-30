import requests_cache
import requests
class drivenc():

    def __init__(self):
        self.cached_session_1 = requests_cache.CachedSession('cache_1_day', expire_after=86400)  # 5 day TIL
        self.cached_session_5 = requests_cache.CachedSession('cache_5_day', expire_after=86400 * 5)  # 5 day TIL
        self.cached_session_30 = requests_cache.CachedSession('cache_30_day', expire_after=86400 * 30)  # 5 day TIL
        self.session = requests.session()
        self.cameras = []

    def counties(self):
        url = 'https://eapps.ncdot.gov/services/traffic-prod/v1/counties/'
        r = self.cached_session_30.get(url)
        result = r.json()
        data = {}
        for line in result:
            data[line['id']] = line
        return data

    def roads(self):
        url = 'https://eapps.ncdot.gov/services/traffic-prod/v1/roads/'
        r = self.cached_session_30.get(url)
        result = r.json()
        data = {}
        for line in result:
            data[line['id']] = line
        return data

    def incidents(self, active=True):
        url = f"https://eapps.ncdot.gov/services/traffic-prod/v1/incidents?active={active}"
        r = self.session.get(url)
        result = r.json()
        return result

    def camera_list(self):
        county_data = self.counties()
        road_data = self.roads()
        data = []
        url = 'https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/'
        r = self.cached_session_5.get(url)
        result = r.json()
        for camera in result:
            url = f"https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/{camera['id']}"
            r = self.cached_session_30.get(url)
            result_detail = r.json()
            try:
                result_detail['county'] = county_data[result_detail['countyId']]
            except:
                raise Exception(f"unknown county id {result_detail['countyId']}")

            try:
                result_detail['road'] = road_data[result_detail['roadId']]
            except:
                result_detail['road'] = None
                pass
            data.append(camera | result_detail)

        self.cameras = data
        return result
