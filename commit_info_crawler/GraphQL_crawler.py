import requests
from datetime import datetime

from get_certification import git_certification

REPO_PATH = 'https://api.github.com/graphql'
now = datetime.now()
now = (now.isoformat()[:19] + 'Z')


class graphql_api_crawler(object):
	def __init__(self, repo_name, headers, user_name):
		self.repo_name = repo_name
		self.headers = headers
		self.user_name = user_name
		self.query = '''
		{
			repository (owner: "''' + self.user_name + '''", name: "''' + self.repo_name + '''") {
				... on Repository {
					owner {
						login
					}
				}
				defaultBranchRef {
					target {
						... on Commit {
							history (until: "''' + now + '''") {
								totalCount
							}
						}
					}
				}
				updatedAt
			}
		}
		'''

	def run_query(self):
		request = requests.post(REPO_PATH, json={'query': self.query}, headers=self.headers)
		if request.status_code == 200:
			return request.json()
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, self.query))
