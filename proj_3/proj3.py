import random
import collections
from collections import namedtuple

class Course:
	Short = 0
	Long = 1

class Weather:
	coldWet = 0
	hot = 1
	nice = 2

class HarePerf:
	slow = 0
	medium = 1
	fast = 2

class TortoisePerf:
	slow = 0
	medium = 1
	fast = 2

course_dict = {
	Course.Short: 0.5,
	Course.Long: 0.5
}

weather_dict = {
	Weather.coldWet : 0.3,
	Weather.hot : 0.2,
	Weather.nice : 0.5
}

weather_string_dict = {
	Weather.coldWet: 'coldWet',
	Weather.hot: 'hot',
	Weather.nice: 'nice'
}

hare_perf_list = [HarePerf.slow, HarePerf.medium, HarePerf.fast] 
tortoise_perf_list = [TortoisePerf.slow, TortoisePerf.medium, TortoisePerf.fast]

def form_perf_dict(l, p):
	return { k : v for k, v in zip(p, l) }

form_hare_dict = lambda l : form_perf_dict(l, hare_perf_list)
form_tortoise_dict = lambda l : form_perf_dict(l, tortoise_perf_list)

hare_perf_dict = {
	(Course.Short, Weather.coldWet) : form_hare_dict([0.5, 0.3, 0.2]), 
	(Course.Short, Weather.hot) : form_hare_dict([0.1, 0.2, 0.7]), 
	(Course.Short, Weather.nice) : form_hare_dict([0.0, 0.2, 0.8]), 
	(Course.Long, Weather.coldWet) : form_hare_dict([0.7, 0.2, 0.1]), 
	(Course.Long, Weather.hot) : form_hare_dict([0.2, 0.4, 0.4]), 
	(Course.Long, Weather.nice) : form_hare_dict([0.1, 0.3, 0.6]), 
}

tortoise_perf_dict = {
	(Course.Short, Weather.coldWet) : form_tortoise_dict([0.2, 0.3, 0.5]), 
	(Course.Short, Weather.hot) : form_tortoise_dict([0.4, 0.5, 0.1]), 
	(Course.Short, Weather.nice) : form_tortoise_dict([0.3, 0.5, 0.2]), 
	(Course.Long, Weather.coldWet) : form_tortoise_dict([0.2, 0.4, 0.4]), 
	(Course.Long, Weather.hot) : form_tortoise_dict([0.2, 0.5, 0.3]), 
	(Course.Long, Weather.nice) : form_tortoise_dict([0.4, 0.4, 0.2]), 
}

result_dict = {
	(HarePerf.slow, TortoisePerf.slow): 0.5,
	(HarePerf.slow, TortoisePerf.medium): 0.1,
	(HarePerf.slow, TortoisePerf.fast): 0.0,
	(HarePerf.medium, TortoisePerf.slow): 0.8,
	(HarePerf.medium, TortoisePerf.medium): 0.5,
	(HarePerf.medium, TortoisePerf.fast): 0.2,
	(HarePerf.fast, TortoisePerf.slow): 0.9,
	(HarePerf.fast, TortoisePerf.medium): 0.7,
	(HarePerf.fast, TortoisePerf.fast): 0.5
}

def select_randomly(probs):
	random_roll = random.uniform(0, 1)

	last_prob = 0
	for k, v in sorted(probs.iteritems(), key=lambda item : item[1]):
		if last_prob <= random_roll <= v + last_prob:
			return k
		last_prob = v + last_prob
	
	raise Exception('Incorrect probability distribution')

def try_random(prob):
	random_roll = random.uniform(0, 1)

	return prob >= random_roll

def prior_sample(bayesian_vars, N):

	course_selected, weather_selected = bayesian_vars

	hare_vic = 0
	for i in range(N):
		course = select_randomly(course_dict) if course_selected is None else course_selected
		weather = select_randomly(weather_dict) if weather_selected is None else weather_selected
		
		hare_perf = select_randomly(hare_perf_dict[(course, weather)])
		tortoise_perf = select_randomly(tortoise_perf_dict[(course, weather)])
		hare_won = try_random(result_dict[(hare_perf, tortoise_perf)])

		if hare_won:
			hare_vic += 1

	return hare_vic / (1.0 * N)

def rejection_sample(query, N):

	samples = []

	for i in range(N):
		course = select_randomly(course_dict)
		weather = select_randomly(weather_dict)
		hare_perf = select_randomly(hare_perf_dict[(course, weather)])
		tortoise_perf = select_randomly(tortoise_perf_dict[(course, weather)])
		hare_won = try_random(result_dict[(hare_perf, tortoise_perf)])
		samples.append((course, weather, hare_perf, tortoise_perf, hare_won))

	def match_post(query, sample):
		for i in range(len(query)):
			if query[i] is not None and query[i] != sample[i]:
				return False
		return True

	samples = list(filter(lambda s: match_post(query, s), samples))

	return samples

if __name__ == '__main__':

	queries_string = '''
	1. In general, how likely is the Hare to win?
	2. Given that it is coldWet, how likely is the Hare to win?
	3. Given that the Tortoise won on the short course, what is the probability distribution for the Weather?
	'''
	
	query_list = [1, 2 ,3] 
	
	while True:
		option = input(queries_string)
		if option in query_list:
			if option == 1:
				print([prior_sample((None, None), 100000)])
			elif option == 2: 
				print([prior_sample((None, Weather.coldWet), 10000)])
			else:
				samples = rejection_sample((Course.Short, None, None, None, False), 10000)
				weather_dist = collections.defaultdict(int)
				for s in samples:
					weather_dist[weather_string_dict[s[1]]] += 1
				for k, v in weather_dist.iteritems():
					weather_dist[k] = v / (len(samples) * 1.0)
				print(weather_dist)
		else:
			print('Query selection not valid')
