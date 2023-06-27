import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count()
wsgi_app = 'projeto_x.wsgi'
