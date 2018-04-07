import urllib.request, tldextract, os

# Ensures we are using the correct code page in windows console!
os.system("chcp 65001")

hosts_header = '# grufwubs combined hosts\n127.0.0.1 localhost\n::1 localhost\n\n# Start of entries generated by download_stripped_hosts.py\n'

def downloadAndProcessHosts(url_str):
	# Downloads hosts and passes them to the method addToDict() which returns a sorted, stripped dict of hosts
	print('Downloading hosts from ' + url_str)
	raw_text = download(url_str)
	hosts = processHosts(raw_text)
	return hosts

def downloadAndProcessWhitelist(url_str):
	print('Downloading whitelist from ' + url_str)
	raw_text = download(url_str)
	whitelist = processWhitelist(raw_text)
	return whitelist

def download(url_str):
	response = urllib.request.urlopen(url_str)
	data = response.read()
	text = data.decode('utf-8')
	return text

def processHosts(data):
	print('Stripping to raw hosts')
	hosts = dict()
	for line in data.split('\n'):
		lineStr = ""
		lineStr += line
		# Skip unusable lines
		if not lineStr:
			continue
		if '#' in lineStr:
			# Skips comment lines and lines blocking specific CSS items
			if lineStr.startswith('#') or '##' in lineStr:
				continue
			else:
				lineStr = lineStr.split('#')[0]
		if '$' in lineStr:
			if '^$important' in lineStr:
				lineStr.replace('^$important', '')
				lineStr.replace('$important', '')
			else:
				continue
		if '!' in lineStr:
			continue
		if ':' in lineStr:
			continue
		if '@' in lineStr:
			continue
		if '*' in lineStr:
			continue
		if '?' in lineStr:
			continue
		if '=' in lineStr:
			continue
		if '[' in lineStr:
			continue
		if ']' in lineStr:
			continue
		if ',' in lineStr:
			continue
		if '/' in lineStr:
			continue
		if '(' in lineStr:
			continue
		if ')' in lineStr:
			continue
		if ';' in lineStr:
			continue
		if '%' in lineStr:
			continue
		if '{' in lineStr:
			continue
		if '{' in lineStr:
			continue
        # Strips any whitespace
		lineStr = lineStr.strip()
        # Strips initial pipe symbols
		lineStr = lineStr.replace('|', '')
        # Strips use of 'www.'
		lineStr = lineStr.replace('www.', '')
        # Strips initial '0.0.0.0 ' / '127.0.0.1 ' from host files
		lineStr = lineStr.replace('0.0.0.0 ', '')
		lineStr = lineStr.replace('127.0.0.1 ', '')
        # Strips use of '^third-party'
		lineStr = lineStr.replace('^third-party', '')
		# Strips use of ^important
		lineStr = lineStr.replace('^important', '')
        # Strips extra '^'
		lineStr = lineStr.replace('^', '')
        # Skips final unusables
		if lineStr.startswith('.') or lineStr.endswith('.'):
			continue
		# Adds the host to a dictionary which serves as the value to a parent dictionary (passed in the method argument), with the registered domain as the key
		ext = tldextract.extract(lineStr)
		base_domain = ext.registered_domain
		if base_domain == '' or base_domain == '\n' or base_domain == ' ':
			continue
		# Write line to dictionary
		td = hosts.get(base_domain, dict())
		td[lineStr] = td.get(lineStr, 0) + 1
		hosts[base_domain] = td
	return hosts

def processWhitelist(data):
	whitelist = dict()
	for line in data.split('\n'):
		lineStr = ""
		lineStr += line
		# Skip unusable lines
		if not lineStr:
			continue
		if '#' in lineStr:
			if lineStr.startswith('#') or '##' in lineStr:
				continue
			else:
				lineStr = lineStr.split('#')[0]
		if '$' in lineStr:
			continue
		if '!' in lineStr:
			continue
		if ':' in lineStr:
			continue
		if '@' in lineStr:
			continue
		if '*' in lineStr:
			continue
		if '?' in lineStr:
			continue
		if '=' in lineStr:
			continue
		if '[' in lineStr:
			continue
		if ']' in lineStr:
			continue
		if ',' in lineStr:
			continue
		if '/' in lineStr:
			continue
		if '(' in lineStr:
			continue
		if ')' in lineStr:
			continue
		if ';' in lineStr:
			continue
		if '%' in lineStr:
			continue
		if '{' in lineStr:
			continue
		if '{' in lineStr:
			continue
        # Strips any whitespace
		lineStr = lineStr.strip()
        # Strips initial pipe symbols
		lineStr = lineStr.replace('|', '')
        # Strips use of 'www.'
		lineStr = lineStr.replace('www.', '')
        # Skips final unusables
		if lineStr.startswith('.') or lineStr.endswith('.'):
			continue
		# Adds the host to a dictionary which serves as the value to a parent dictionary (passed in the method argument), with the registered domain as the key
		ext = tldextract.extract(lineStr)
		base_domain = ext.registered_domain
		if base_domain == '' or base_domain == '\n' or base_domain == ' ':
			continue
		# Write to whitelist
		td = whitelist.get(base_domain, dict())
		td[lineStr] = td.get(lineStr, 0) + 1
		whitelist[base_domain] = td
	return whitelist

def backupToFile(data, file_name):
	print('Backing up host list %s...\n', file_name)
	if data.keys().length() == 0:
		print('Dict empty. Not backing up.')
		return

	f = open(file_name, 'w', encoding='utf-8')
	for d in data.keys():
		hosts_dict = data[d]
		for key in hosts_dict:
			f.write(key + '\n')
	f.close()
	print('Finished backing up.')

def compileAndCheck(blocklists, whitelists):
	hosts = list()
	whitelist = list()

	for whitelist_dict in whitelists:
		for key in whitelist_dict.keys():
			for host in whitelist_dict[key]:
				whitelist.append(host)
	whitelist = list(dict.fromkeys(whitelist))

	for blocklist_dict in blocklists:
		for key in blocklist_dict.keys():
			for host in blocklist_dict[key]:
				if not host in whitelist:
					hosts.append(host)
	hosts = list(dict.fromkeys(hosts))

	return hosts

# def getOrderedKeyList(d):
# 	l = list()
# 	for i in range(0, 10):
# 		if d.get(i):
# 			l.append(i)
# 	return l

# def getHostLengthDictionary(d):
# 	return_dict = dict()
# 	for key in d.keys():
# 		s = key.split('.')
# 		i = len(s)
# 		return_dict.setdefault(i, list()).append(key)
# 	return return_dict

# def getUniqueHosts(d):
# 	# Returns a list of unique hosts for each registered domain, that don't overlap subdomains (e.g. stats.facebook.com and s.stats.facebook.com), keeping only the shortest.
# 	# For each registered domain, goes through the listed hosts and creates a dictionary with {"Number of domain levels" : List[domain, domain, domain]}
# 	length_dict = getHostLengthDictionary(d)
# 	return_list = list()
# 	# Creates an ordered list of keys (which are the domain level ints).
# 	key_list = getOrderedKeyList(length_dict)
# 	# BUG: another hacky fix right here to account for key_list sometimes being empty
# 	if len(key_list) == 0:
# 		return [""]
# 	min_length = min(key_list)
# 	min_length_host = length_dict[min_length][0]
# 	ext = tldextract.extract(min_length_host)
# 	# If dictionary contains the registered domain (so all traffic should be blocked), returns only this.
# 	if min_length_host == ext.registered_domain:
# 		return_list.append(min_length_host)
# 	else:
# 		# Else goes through the dictionary and finds unique non-overlapping domains
# 		previous = list()
# 		# BUG: this for loop seems to create duplicates in some instances
# 		for length in key_list:
# 			current = length_dict[length]
# 			if length == min_length:
# 				previous = current
# 				return_list.extend(current)
# 			else:
# 				add_to_return_list = list()
# 				for host in return_list:
# 					for entry in current:
# 						if host not in entry and len(entry) > len(host):
# 							add_to_return_list.append(entry)
# 				return_list.extend(add_to_return_list)
# 	return return_list

def main():
	blocklists = list()
	blocklists.append( downloadAndProcessHosts('https://filters.adtidy.org/extension/chromium/filters/15.txt') )
	blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/piperun/iploggerfilter/master/filterlist') )
	blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/quidsup/notrack/master/trackers.txt') )
	blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/blacklist.txt') )
	blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts') )
	# blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/Yhonay/antipopads/master/hosts') )
	# blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt') )
	# blocklists.append( downloadAndProcessHosts('https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt') )

	whitelists = list()
	whitelists.append( downloadAndProcessWhitelist('https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/whitelist.txt') )
	whitelists.append( downloadAndProcessWhitelist('https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt') )

	dir_name = 'backups'
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	dir_name += '/'
	file_ext = '.txt'

	hosts_str = 'hosts_'
	i = 0
	for blocklist in blocklists:
		file_name = dir_name + hosts_str + str(i) + file_ext
		# file_name = os.path.join(dir_name, '/' + file_name + '.txt')
		print(file_name)
		backupToFile(blocklist, file_name)
		i += 1

	whitelist_str = "whitelist_"
	j = 0
	for whitelist in whitelists:
		file_name = dir_name + whitelist_str + str(j) + file_ext
		# file_name = os.path.join(dir_name, '/' + file_name + '.txt')
		print(file_name)
		backupToFile(whitelist, file_name)
		j += 1

	compiled_hosts = compileAndCheck(blocklists, whitelists)

	print('Writing hosts to file:\n')
	count = 1
	f = open('hosts', 'w', encoding='utf-8')
	f.write(hosts_header)
	for host in compiled_hosts:
		# Final dead host remnoval
		if host == '' or host == '\n':
			continue
		host = '127.0.0.1 ' + host.strip()
		f.write(host + '\n')
		print(count)
		print(host)
		print('------------------------------------')
		count += 1
	f.close()

if __name__ == '__main__':
	main()
