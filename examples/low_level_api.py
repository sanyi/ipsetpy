__author__ = 'sanyi'


from ipsetpy import ipset_version, ipset_create_set, ipset_add_entry, ipset_list, ipset_test_entry, \
    ipset_flush_set, ipset_destroy_set

# getting ipset version banner
print(ipset_version())

# creating a set
ipset_create_set('test_set', 'hash:ip', exist=True)

# adding some entries to the "test_set"
ipset_add_entry('test_set', '192.168.1.101', exist=True)
ipset_add_entry('test_set', '192.168.1.103', exist=True)
ipset_add_entry('test_set', '192.168.2.0/24', exist=True)

# listing available sets
print(ipset_list())


# check if ip is in set
print(ipset_test_entry('test_set', '192.168.1.1'))

print(ipset_test_entry('test_set', '192.168.1.101'))

print(ipset_test_entry('test_set', '192.168.2.21'))

print(ipset_test_entry('test_set', '192.168.3.21'))


# delete entries
ipset_flush_set('test_set')

# delete set
ipset_destroy_set('test_set')
