# -*- coding: utf-8 -*-

def is_auth_manager(u):
    return u.is_authenticated() and 1 in u.groups.values_list('id', flat=True)

def is_auth_direction(u):
    return u.is_superuser or (u.is_authenticated() and \
                              2 in u.groups.values_list('id', flat=True))

def is_auth(u):
    return is_auth_client(u) or is_auth_manager(u)
