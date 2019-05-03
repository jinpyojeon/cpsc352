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
    'short': 0.5,
    'long': 0.5
}

weather_dict = {
    'coldWet': 0.3,
    'hot': 0.2,
    'nice': 0.5
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
        last_prob = v

    raise Exception('Incorrect probability distribution')

def try_random(prob):
    random_roll = random.uniform(0, 1)

    return prob >= random_roll

def prior_sample(bayesian_vars, N):

    course, weather = bayesian_vars

    hare_vic, hare_lose = 0, 0
    for i in range(N):
        if course is None:
            pass
        if weather is None:
            pass
		hare_perf = select_randomly(hare_perf_dict[(course, weather)])
		tortoise_perf = select_randomly(tortoise_perf_dict[(course, weather)])
		hare_won = try_random(result_dict[(hare_perf, tortoise_perf)])

		if hare_won:
			hare_vic += 1
		else:
			hare_lose += 1

	return hare_vic / N

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

	samples = list(filter(lambda s: not match_post(query, s), samples))

	return samples / N

if __name__ == '__main__':

    queries_string = '''
    1. In general, how likely is the Hare to win?
    2. Given that it is coldWet, how likely is the Hare to win?
    3. Given that the Tortoise won on the short course, what is the probability distribution for the Weather?
    '''
    
    query_dict = {
        1: [prior_sample((None, None), 100)], 
        2: [prior_sample((None, Weather.coldWet), 100)],
        3: [rejection_sample((Course.Short, Weather.coldWet, None, None, False), 100),
			rejection_sample((Course.Short, Weather.hot, None, None, False), 100),
			rejection_sample((Course.Short, Weather.nice, None, None, False), 100)]
    }

    while True:
        option = input(queries_string)
		if option in query_dict:
			print(query_dict[option])
		else:
			print('Query selection not valid')
