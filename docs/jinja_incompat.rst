Filters
-------
- join, default join character is " " and not empty string
- map, mosty works as before except that it does not call filters with first
  argument but always treats that as the attribute argument.
- round, if precision is set to 0, we return an int rather than a float.
- sort, we sort case sesitive by default, jinja sort is case insensitive
- sort, reordering of arguments where attribute is first instead of reverse
- truncate, reordering of argumets from length, killwords, end, leeway to
  length, end, killwords, leeway.
