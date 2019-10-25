#!/usr/bin/env python
# coding: utf-8

# In[28]:


from datetime import datetime
def get_days(source):
    """
    Inputs:
      source: string in format 'YYYY-mm-dd HH:MM:SS', base time
    
    Returns:
      res.days: an integer, which indicates the days between this moment and source date
    """
    this_moment = datetime.strptime("2019-10-23 20:00:00", '%Y-%m-%d %H:%M:%S')
    source_date = datetime.strptime(source, '%Y-%m-%d %H:%M:%S')
    res = this_moment - source_date
    return res.days

