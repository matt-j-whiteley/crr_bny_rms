import os
from datetime import datetime
import multiprocessing
import socket
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

from main import main_func


images = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAJwAAACUCAYAAABm60AgAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAB5MSURBVHhe7Z1rsGRVdcdXv+69fec+'
    b'5gUyDDMqCkGJUJFoGHwFglAVE6MlBRrxEdTSJPoxpvLFR75YhUnK0kqqrCQEU5IgFqhIYRzG'
    b'GUdARQiUoDJhAKlhGGZgZu7cx9xHP7P+a+91zj6nT9/bj9N9T/ecX9W+fbvPs/f+n7XWXnuf'
    b'05k6QykpsQE5ZeyrCz4jysrflJSugLi0+NTrVSkuqYUbWtCsxqp0RlgWq+2rLsLKZCr8f1ne'
    b'E41wGfUEl8nkzWsquGEETbrCZZQLC6WGzyzwaXjPr2p7cviDz3S9vG5f4gLh8B7reapZ0SjZ'
    b'OgQGMS0SLT1LK/MPUf3Fh+jk8Wfo3F2fp3rx7Z7QlFRwQ4k2adAq1T2BQGJWiBJULeMPLbH0'
    b'RqhgBGhWNcuzRoBYDooi1Tne4AjNzvyGaOFBqpUP8PvjNFp9nMqlV9P05f/Ih7iWqvlxu5Uh'
    b'FdwZgXF5wLg9Y7EyVbY+LKg6f4bPqzQmyzyLFyYLYb7E+nyClg/dT9WTv6BK+TkqjPxWFo+x'
    b'Qa1XRmhhabsIrp7/U7GKsIQq8lRww4pnvXyxKabxmZpjAWVdg7u2EQuLrPw0rcw8SStHHqDs'
    b'ypNUrB+lXGbWrFQpsErVJBLNlrfS9Ju+RvXRa2k5U7cW0bj3VHDDihWculE3/lIXh2Vq8WDd'
    b'1LIZi8ciY1HVF39JSy/soZW5X9EUHWBdsXBgGSEwFlM1V6LcygbZh4pOBUdj7xKpGdGa46eC'
    b'G1ascBQILue6SbFoJnaDewWZzBK/eZEqMw9T5fgT4jIzmX2ybJwmsMMGsQERofN+njsbGy+9'
    b'i6jwHhZcxhzXWtBUcMOKZ6kqIihXcObzRe4EFK27O0m0eICWj/+c6NQTtDL7EE0U2HKhYwCB'
    b'KfmyJyolV+VeLAuxmkev1qAxHATHEpNzSQU37Egjo2ltesTGa767XODWH6NZjskyL/2A6vMP'
    b'0vTIyyIegS1WbXSBsnPbWFVsCUNiE6tmqbKzBRLT8fal8nk08qYvE42wS2WhpS51oHCbxwny'
    b'm4L1/fU0hgPiMmnG9DJf+iUVjvyLH/iHqNan5XUl8wKN5kwuTq1ZABZmAO5AlGrnBASXE9ed'
    b'dhqSiXV7cEFwdqaxkL3nnqBjqQS4KV4fjaoYa1KRnNkYi8ONy0rH76XysZ8Zd9lEaB0BETrC'
    b'my2dZToNnuD8iyAVXNJQwblYQWmPD5jepRGi9DA9oaI57SjB4iNUnbuP5k5w8L+0lyYr22UV'
    b'dX0N1qlTUsENKkYsnnVC79EVIITHxU81mA4BMAJEvuw5qpeeofmDezn0esFLzMItenFXXEJT'
    b'UsENKnUWm7Fgxh2a7LwQcrXApBvY5dYPics8ffynlJt5iKqlkzRRfMGPubSnyYF/T0gFN8BE'
    b'CKskrlPHMAEs1Ysc/D9G1VMP0NKJR6l68qCfymCQpvCStMDmzgQWCHqWsm4c1i4V3ABjDBzV'
    b'WSAYFsJgOpDOA1syWjpM1WOPUmmGy+mfB92lmzNzBaZAGEocQlMwtKXWk4/hjTSkghsA2MKZ'
    b'RkLv1FgrzMqonnyKyi8/SJWVB2mi/pT5HERYMMmXVc5iEbws7xVxsb0gFdwgo0Lj18Wnafnw'
    b'bo7P9tBE5VlZKrixWMidecNNrrhC68ROKri4aVZFphKD6LrusqjPfPxBdJPKwBBTZX4/ZRd2'
    b'03h90rNi1dHTlMmXaNmOInkJWXWnsHJAxQWhAdcKunQqwrCA3fdNBQfSxG8LNE7vUdCLxOC0'
    b'i3GFTG3M6wAgHhNBVfgzbgDkyrCdSW0s8gpPU+nYPqq99AgVFu8PJmXDjbsaUeuuJo4wWKY4'
    b'AvKIEjUDqyoWdYUvjpEFT3DVsXfJ8nSkoW1QRU7Fh4Gw3N4lRBUBepte9n/pGZmSXT31E6rN'
    b'/J+ZX1binYzO27WTQXiw3kXdNsZcMfFSLC0LcZEWaPzSe1LBdYcVnSsuxlgvFlCFHQe7OLV6'
    b'msqQKdu6fuZRmV9Wm38qmMqIc5ipXVazeKuB7azF05kiKjg3LSLITOFUcG0QdKsy88GxaP69'
    b'AuYVIwVFFpqJzY7IYHnp1AEqP38/VZYfD4rMuqzFzDyVckQbqxPyvi+47rKZ6Nx1olA362wf'
    b'EJxY+1RwbYDqYZdRLxqhMdERncFLZ9QP08rLD1P96I+ptnS7LJNJjOjRudjGgutaqZbMOv0g'
    b'LCRXcM4ySSCH0ikNPWG3l8qI4C6/lVd4u5PiSQXXIvaeSx3X5BcIDpWoExur5RqNFA7zqsep'
    b'MvMkVQ79ws+XWTG5jebGRS0lbHtBi9atNjZP2RV7EfB7GaFg6xwV2+GCATW6jCbecDNfYVdK'
    b'eKFT2kEquFaAp4TrZJdpepvWn+ZP8YdHuaZflLuYKuXHJC6TiYwAjcpiqubG5S2GkmAxkNoA'
    b'SG80jBL0S3BARRc+nj1vORfXZeJzftW5ctWymXhZLpxDmc3bOGrdSBNTU1TJvopGz2KxZS6U'
    b'5ang2iSQJxPYRSD7f3QPLS3eR5Wl3Sb2sg0iuI2GRoKVw80mzvsowu6rp7jnq+hn1vVjMiVY'
    b'ErfI1qs4SaNTv8vX3w7KbHw1jU5cwNvsJNpwNtfTOGVg5fJ4xENRrL/fMzcX1JAIzv0KXGFt'
    b'oduuth0qm2MUZyIj7mLCTb+SmAUhcSmegLQh8QrUogFXlFGCC2+L/9tBtwO6nyb7UOsFchvO'
    b'o9nRy6g4dT5lR87hmjqbCpsv5iWTIiglkznJf6fYfdo7vxhcpCq4Yo3Fa1NFgys4GBx8iayN'
    b'sdgCyc29uJKcHiRwg3ypELvcc5EAiVpgtzEig3BOUenotyUpi5tLMFju3cGkuGKIwooLIwVA'
    b'RIX1VaRKMyGF1nVvWFHCQlXR6+cQkrh0nSXC+1vMz9D4+B/QQnaaqoXXirCWattoetPriYpn'
    b'81Y4b+M2DSbwb0TPe5U6sAyu4CAaEYcvuGjQe0KKwt5pDvgFIpSrD64jJFy9u3z20L1Um3uA'
    b'CtWCN8cMeIKxrNaTc5FYTbHiCq8X3o8SaTWBnocrXrtvJGAB0i2gXryKRjneyo5dTGMj5xFN'
    b'X2IW1PgC2gBhwWqZupKP+eJ14684GFDB4ZRXrEVDlXCle1bNFY55ek/A+jGuxdOZsyKyxaep'
    b'NPeYP8RUXZR1JOi3My+8xtaGdq1S1Gcujkg9VHjWlel8NqFFUcpyzA5hFsrcCRnZTPmxSyiT'
    b'O5dGt3LgPsXiymwmGuPvkbGWXDhb3OBqpIITcMqO4EI3lpi0BQMdifUyn4lFs3IzFo8bKndA'
    b'8mXLpx6X2bIyxGRdTthioGGjBCefu9arCV5GPrwPtbwM3C7SCw13SjnrAFwESxnuHWbPo8r0'
    b'dpoovJrq09soP76R64Mt1fhreS0WU4WtV9b0krUecJFhrp2LzrsDvsiwTsRF0gUDLDhUhH/q'
    b'sGSKVqa6Sx3bdAfLJV9m7y7HvH+kMjxBoYGtkEDAooStlF1Pc1ABoQBnfc/16mfa6PqeRaVx'
    b'HsA+8SQiWCwIK8siy0zspPzWNxhh5bjDkmdBZbby2pu48P988ZWqNcoV7Jd2aLRWbtPbc2BP'
    b'gdgWmB4n3GzoO3fB4MZwDjq0BFRsOoZpOgbci6qf4hY8KPdjVo+xyDDEhHn/dvxPGt1uq0JT'
    b'mlovZ321SgHr5O5bLZTTIwUqVAgLwBWqsLJTZ0nvMD+5gxecw9uxoFhUeuMxwEUEwpYe3xsx'
    b'mOJPEeJl9uI04Yj8Z18VE5YAL2SJiaEQnKAxnEWERs+ySzkqT/3BEJP2MlUQLg2ui4XhucAo'
    b'wVmxeaiVCqOCY3BHOkBOC1Yru+l32MlvpNGx7TS6ZRtlRthqFS7jNXAOKIivRoz7Z/FAAgEr'
    b'5cWt5sXPF+J/8z18UeGzYOdK1wFYj5fadz6B48XAEMRwXGla8TV2l8j+L70kU7JXTn9P8mUZ'
    b'epwmueFEOCFBqUUKCK7KDe083sBbFhaZ4grVghhLA/hyrkyF4jlU3PJGk4XXZOnouSyWcd5c'
    b'hcLH4zNdCwkt1WPKq3aUfIulVl87SmvhByRBEi443VXjlbI6rW7nnyoq2HTb8RksUTCVIUnZ'
    b'CuIaJhT8e0AoJXZTUc/OcAVoB6YbXC3WsRl55LSQfqjTJZKJz0+9kUY2XsSi2sbHRYwFa+Un'
    b'SxWZFABLg4vGE5FznnCT+rkNEVyau0UjIixVy9dwgdoefTNaFWs7xCg41+/bE9UvpqDibMW6'
    b'X7MhDvEqhNfTymZ0PUVis/IBqp74Ac0dvteIzE3KQkwAgrKxUxhJR4RuNlFEUMCKCsJDbkuF'
    b'lctfQhumL2Wvt5Nymy9kPW3mlSAs1xWqIICKInwejWJpTifbutuE12/W/O2cU+v0zsK5YhPR'
    b'uPkxbhDnKsP6rgDNdBa7jic4rIdE5jz/e5SWD95B1dkDVK8dDjyN0bVCkfP/VUQOrtv0ngRU'
    b'XRS3iAHqpVdcKXFWZmyLcYfIaYm4cGHpRcDxV0BkboPpd4/fYgwaPYzhXIvnWybTIPqeYyq2'
    b'aBrD6EONkS8D3mxZxGZljsmcKdmBu5hcEJtpLy7CcjUIDvPwmVJmI5XHLqTc9EUyKL1cmaTp'
    b'bewSl1nxXsIUouJ98zmp5dVzDd6k3GhFUsEZeiY4t8cEIDSgz3wNxxMqOnxuYjNYMjNYjkcY'
    b'5E8+yTbvKW8uViD9YK1TU/iYYvkqZ3nJ0lzhlVSY3uEnSzWnBZfM4tPBaGAeqcDFnitArgto'
    b'vssPC6JElQpO6angFLgYrm4JYMUl2gSl4DSkER3HZcsPU/XFJ2n5+AOSL/Pmlynq+qwFc+eX'
    b'KchrIaeFXiIGoguFrUZcoZwWngIZpiiuUgkJWUVnLVxrvcFUcEpPXarXWNpIeMWPTmjHAI0m'
    b'DXeEFWKekl0/8ht2nd+n6cJxLDAg2A9ZMHWbiLEwAbDKMdbI+HZJlhYmN5ucVv5i3hbWaowb'
    b'fFwaXB2f5woxdcbFCsmHraP9HuFOi8tagjOExHsGEqPg9Cp2AmYVlfvKeJasfspzmUhlyFOy'
    b'2T1qEK+uE+gQT754AdXGsjQ6tZOFsNVk4ossrOL5nqjUnatLhFDUvavLBmJxXQ2p2OyrWi9/'
    b'fXRmfAJhQYNQU6KIVXA+4SsZDQWLgkd+8v94hMHxn9PS/I/kQXkj1uyM1s0D85AwxcxSJEuz'
    b'7Aolp7XlfF6yxbrDjdzY6CUatMOBmaUm/jO4bh14FwMEoiIRoQSrQDs7ime97AUTiZs7C5Ba'
    b'NZfeWjhpSMRsC/zvUZp9kS3YzDfMIww0KVsdo9MjFxmXuPl1NHb2pVRe5P7pplfybkzwbiyJ'
    b'2a9aL5kw6YjFFUmD1VGh2PdYU62Vv28QEoeznStBHZdUV4utw+IGwbpIAbHGcEtsxcz8dVT+'
    b'HH9whCpLv6bFQ/9D1crjsk526q0ys7SenaDRTa/zLJZJlqJx7GTJVRsLp9xtQ+rX7mQ/3Wx7'
    b'ZhNvp0Eu8kWilSNUXvktLS6bXuT4GAfyxbPYYnDPUGaWsrgqbIV0nhZgK+JZLxt7pQwfPRAc'
    b'sIPo8gHEU6RSeQON5NTHGdxhK+PUotxyyjARr+AiCIbfwZ4eAn0gIwr4JxRrpQwfsXYa9IHI'
    b'INBjdAP4UGoBeOkFEFg3ZdiIVXBmmpAREPBExGgvzrtzCqISYfluFL0+Y/NShpV4Xaq6RBcr'
    b'KhWjPJQPqBVz8lep4Iaf3gnOE1ow+E/zVWc2sQpOOwjGShlXCVzXGkygppxpxGvhImm0ciln'
    b'LhpJ9ZBUbCk+fRBcSopPKriUvpIKLqWvpIJL6Sup4FL6Siq4lL6SCi6lr8QrOAxtaRGQ9A2X'
    b'/oFhNC1Nj+2es3fe7ROehiXH0/11uW+XqKHBTimVaxHn3Vt6M5YakLHZfdQwV6/BEc39B6sk'
    b'n10hhM7bvWehY5ruv1PW+D5tYOqnv/TBpaJycJ9Dzg7Sr0V8+jdHCz63pCkNNWFmrnQttthr'
    b'OL6RG3w3WLl+0puxVP4O+iiE9WSkkA1UKN43wIvnTi/Q1IaJ2M9Zjx953KasbZHjPE/vHDH9'
    b'P/aLo5GeCO6W/7iV7rzzO7Rp02aq2srRKurDd/JYKZdohD14JjNC01MT9NWvfa2hYlHZn/3s'
    b'Z+nQ4RdofGzMO1/Qzjm7EijzcXeet51uvvnmNsUG3OZoFN7PfvEwfelL/0Abit3faJTjuqhU'
    b'limfH6OvfOWfaOsWe+tmD+lZ+48WzR1Z+FKZXI5ftfAh82zMmxQsb1awn1YL1h8tFilTKIoY'
    b'Xjpxku6++3veNzaWry6CuOEDN4gwgXusrJyP2Vd4/24x2/jrQ7gHDx6kBx643+y0Ddz7a8Ph'
    b'Bc75G7fcKmLT83RL1Lk1K1hf9sl9kA996IN9ERvomeCUmhcF4VBZqmZWj0GwvMZXdlRpB1m/'
    b'wmE/txmEABH81+130PETM7IcQtPG3fXmN9GuXVfI1e6izy9c69jmO3GD1011Yn1Y97vv/j7N'
    b'zZsf5wiLJxqzTlB0Pvv27aXnDx8WwWiduKUdcM6w5rDEu3ZdHjTRPaTngjP4h0GjoCFXK3GB'
    b'hqlWjehU6N+64w55RZO6nZgPfvBGudqlIey65rzXrqKoc8Y+YOUeeeR/zfs2BREWHYT7nbtM'
    b'mBIHOOe5uVNi3acmJ9ZBCT3AXHXhS6eVS0kbuvsCF6fAxd7/kx/TM88+F+p91sWl/Pn7r6fT'
    b'86cjBBS972AJkuPQ2LVyweM1wxdluEe/e/d9dOSY80SpyHNopRhwIe664i1i3dEkJsToPf4Z'
    b'xELjpW6esoUvU+ODRbuKRsz68RQDRIRS5w7ELf/+b3ImYnVkNdPQ11zzTpqaGKdaZUnOu1o1'
    b'j/QK7m+tYlA39+xzz4tYQKtJW4jNWERzfhDsnvv20IbJDbJPQ/i44QL896h7U+pSFti6fYAv'
    b'MCFrYtl+EOtRwm7AiC1ZwOI98ZuDtH/ffmN1nBqAa7nppo+KawVYt57RxuuMiYkNdNd3jZVr'
    b'PeltKk5qk88PgkWnJ8p1N6f5eS8uL9P73vdees35r7KWrX8N1R9ZJ4wi9/Lu+NYdJqB324X/'
    b'v+rKd0ggXeMOB9COQDcsLy95Vm4tjCuty8WAgnP89p3flXCgWzTlgw7UddddJ//3y7IpZ6Tg'
    b'YLlgMUQEqAGtBfuKQDouECuNjRWlh7x2nMQmjN2728HAOSKvB7CvbkAqZG5hUdIg0lFYB85I'
    b'wQGI4D+/ebuXJnFBIH3F5b/fdQMD7bRUKjWTBwQNuoOvtP7SaRGcG4QKiwR3mssV2j4nhDWI'
    b'2QBc6RtefwFdeeVVq3ncnnLGCg7k81m67bZv2ncmZtLmRJqkwBah9Y7O6iCWu5Ndowica923'
    b'dlZojMbARqLkCdTNsUF0rRIVQ9/0sY8bN7pOLX9GCw5Wbv/9P5U0iYLGRrNv3bSJ3vOed9PM'
    b'DH7P3VDv0uKdXlr2RBR+dFm4wwVh/vC+fWLdOiEsNli3d7ztCqejsD4MkeA6+yqjBZMmQSOo'
    b'ZZFX3h3SJDvOM78ACJBI7gYMSe3du98I3DndqJEFCFNjN7Ny900Fqw2ifku1X6zfkdsEV2y4'
    b'6OeGWsPycFHczxBII02i456m6Y2bQ2D9kZs+SrMzJ+R9t2jQvn//j+0nwEzdcoEg77PWzZ1M'
    b'0CmVyjL9yR9f27fx0tVItOAgCATJCHrr5aXGAhdXqcqrJGuj1nEK1gmvh8YYH8tKmgRuzDS9'
    b'r050IC644AI5hivUTkFiGWLy3LijJxXef3NHATNdELsZq4qV3LI2gSHEQpFuvPHDdom14E7s'
    b'2E9inZ6ETDqSm5iedM+9P/RyR5qwhHDcAHgtxALx6X3xi5+nHTt20vLyonw+ht++ignsE/vD'
    b'a7NUAcTxN3/7d4FcmPlOuF5bEwBwe4t/dNUf0l//5Sflvd/4Ge9YBXb17rBcu+BCxfbIAX7y'
    b'Ex+ja6+52i5RcMwurpwOSbSFQ/K1zC5lenpaelYQBAr+j6vo/pqJDSDQhkBWlvA7Ey4QW+tV'
    b'qBcbXOWP9poxXR+zDNatW7EBbA/Rve7C19DVDWJbPxIpOM01YVoRUhMKPm0Mr3sPjnnD9deb'
    b'HqOd8hR0q+2LDqK6557vy/8qNgjwZz99UP4H7ebcXLAtOh1Ig3Qn3XhJpOCaXd34dD0qD8dE'
    b'wI0MPab0wDVqmGBo3a0CTF3CxbR79x7PyqGXDOs2MbXRs06dWTnTpBAbrDJCkWgCV0zfSKTg'
    b'XOLopcUFJiqiAwGkI8Nt5s8oaR/MiobIwPPPHxLrpiLrRGx6PnjFDGZYZYQL65l3C5N4wSWD'
    b'ujQa4jyMs2oyGB0a1+WvBYTgumJ0Qh597DGxchDeFFu3boDVhVAxp++6664XqwynPFJwDrrO'
    b'DLDg4NPiKK0BSwFkOvoVbwlMR9feZztAHCiI5b5885fp17/6NYul8+bQeA+vGEZ77/veK2Iz'
    b'djIV3KqoJQjGSetHeCQAExfn502KpltgkeZOL3UlNoD9aEfh4zd9hIVWl5/tjPNO/ThIpODy'
    b'tRyLje2GvWobMQ+sjqO0QngkAGkSTGBEPg1k7O9SrIVatagLCb3XdnKULq6rRhoEc/r4KJIT'
    b'7eeTDlohkYIDOa7BTK7Q5Mr3K7Pb0invfvef0dlbzH23+MHh9cHUjStgpEGSTGIFV+Va1KlB'
    b's7OzMvO1V6UTEJBf/c6rZQbI+oCmM71PWDckpd9uZ4MkmYQObbHUuHuvqQFs59+6Z0APMQ5e'
    b'uXM7ff4Lf+91CqLBsRrPG2L93Oe+QMeOvdz1TJL2CQoO9aF3z/udheSRUAtX88QGILaouKdb'
    b'NMe3uthA9EWCNMlnPvNpSQavJ3MnT8jNPzobJKliAwkVXJDVguzuiqGbxChc2DXXXC09RGOZ'
    b'TRigr73DWjc+DpLRb33r2+R90hkIwSkQnpYkoJLCxEbc56lhAMTmWuhegDADBTGkPBtlTSud'
    b'DBJ5ltrNjypJA6KDK0OaRGfo9kNsACEBboqRu+cdkpZ7cxk4C6dEibHdggH0zsCJmMQqCv7H'
    b'fZ4mTdJrV+qDSZqNaZCEmP8mJFJwrut0S3JgtXLxc3kZ6UBcf8P1YuXU3ZnqdUt8YKo6po0H'
    b'0yD+LzgmlUQKblBB4I5Mf69nuGD/575iqySffZIvNjCwgouygO2WuEHgDhfnJ4MhvPjFhzQM'
    b'rKmkQZzdh4fgksgZbeH0+SFxggmP115zlTfOGjeIEQNpkFALQnRJFl5iBaeBvf7vEn7vs/5f'
    b'B1YOEx/xaAfEcX4nIh5Lh/QLks2NaZCmlZIoEik4V1D4H5YIr1qa016j6pePK4el0oKr+/CN'
    b'75fA3qRIOheb2+vFHViYi9d8vBSVs2oFrTuJFFwY9PwwOO0WVP5aRe4lXaUgrRAfeMSWHxgi'
    b'oEdgv/oFsjZuTg+PpvjUJz9h361GckWXyMH7cCNdfNFFNDnR/fPRopicnJSbhLu1cvrdYY9U'
    b'Inv37aev/+stXSWCddQCFxDSIDf9xUftksFkIAT39X/+6qr3jSYDrUb/5PWmZtRDN71iiA5W'
    b'/tN/9Sk7uRI7W7sek0giXSqm2mjBfaClUud3RvUPCKBRBHhYjvkurVm5xjg1692oUy5rPQym'
    b'2MBAxHCDTPdxYq0lrzAopIJLPMPVRKngEk/8IxXrSSq4lL6SCi6lr6SCS+krqeASz3A1USq4'
    b'xDNcnYZEP3JVwbMyihvie8xqJ1z2e5c1Gf7S6mv8XjrSYH7YI0/VzNrToTTp649M4Jg1GdqK'
    b'fnTqYJFowelMCQzrYLpPt+CHQMK0st/zX7XD+TlxfBn3O6SCa4eoSzYx4FdXMHCNWRJ4BFW7'
    b'BT/36BZcAOEStZ1bZNtx98c5Wr9gUhpJtOCGLX5JSajgwrNFOgVuKVzaRbeJa5Jm+6QjDT2n'
    b'E2G0iiu+Xh4nJZqEu9SUYSMVXOIZribq67cJP+MtpRXSGK4pyMEp+J0AxZ3Fqv8PUlkdrIAS'
    b'HRBixq8Ste9wUdzP8IN0w0Ksgls7rXnmgucAt9JJierQ4NcAh4WeudSS88QotwLdCk1qcc8z'
    b'btzjRBXTJKZZzHv/dRjomeAAbh5xK2tQKi7O82z3ngY8vd0Uc9PNMIkNxCq4zu++HAacAMzB'
    b'jeHawTzF3S/DQs8s3MrSojzQRe+CH9SCu/xPL3b+YBo86Qg/k4QStf9wOb2yIGV5+bTUHx7N'
    b'hVfU5zAQ62wRDo25ZOiHu/fQgQNPmo+GANyd38kd7/hJ89tu+6Z91z1vvvzyhserDhqxT08C'
    b'bnokxe+9n9khh6EngnPBs8qqbU7pcR8KA6Ke7Bh+Blqnv5vVbDt3vVK53sHgfV2+t3kGcONx'
    b'QfjYZp3ounLrdpAv6JhdakrK6vQ0LZKSEiYVXEpfSQWX0ldSwaX0lVRwKX0lFVxKX0kFl9JX'
    b'UsGl9JVUcCl9hOj/AVmbT9BFNXh+AAAAAElFTkSuQmCC')

now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

def check_ey_pc():
    full_pc_name = socket.getfqdn()
    if 'ey.net' not in full_pc_name:
        wx.MessageBox("Please note that this CRR tool will only run on an EY-owned computer. If you are attempting to run this tool on an EY-owned computer and are getting this message, please get in touch with the UK FSO Assurance Innovation team.", caption='Warning')
        return False
    return True

class frameMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Data Automation", pos=wx.DefaultPosition,
                          size=wx.Size(688, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints((680, 550),(800, 650))
        self.SetIcon(images.GetIcon())
        bSizerFrame = wx.BoxSizer(wx.VERTICAL)
        self.m_panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 20), wx.TAB_TRAVERSAL)
        self.m_panelMain.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))

        bSizerPanel = wx.BoxSizer(wx.VERTICAL)
        bSizerPanelMain = wx.BoxSizer(wx.VERTICAL)
        bSizerDir = wx.BoxSizer(wx.VERTICAL)
        bSizerIntro = wx.BoxSizer(wx.HORIZONTAL)
        bSizerIntrod = wx.BoxSizer(wx.VERTICAL)
        self.m_staticTextIntro = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"CRR – RMS RECONCILIATION",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextIntro.Wrap(-1)
        self.m_staticTextIntro.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))
        bSizerIntrod.Add(self.m_staticTextIntro, 1, wx.ALL | wx.EXPAND, 10)
        bSizerIntro.Add(bSizerIntrod, 1, wx.ALL, 5)
        bSizerDir.Add(bSizerIntro, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        bSizerDirHor1 = wx.BoxSizer(wx.HORIZONTAL)
        sbSizerDir1 = wx.StaticBoxSizer(wx.StaticBox(self.m_panelMain, wx.ID_ANY, u"Please choose file directory"), wx.VERTICAL)

        self.dirPicker1 = wx.DirPickerCtrl(sbSizerDir1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder",
                                           wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        sbSizerDir1.Add(self.dirPicker1, 0, wx.ALL | wx.EXPAND, 0)
        bSizerDirHor1.Add(sbSizerDir1, 1, wx.ALL | wx.EXPAND, 10)
        bSizerDir.Add(bSizerDirHor1, 1, wx.EXPAND, 5)

        bSizerPanelMain.Add(bSizerDir, 0, wx.EXPAND, 0)
        bSizerSplit = wx.BoxSizer(wx.VERTICAL)
        bSizerSplitHor = wx.BoxSizer(wx.HORIZONTAL)
        bSizerListbox = wx.BoxSizer(wx.HORIZONTAL)
        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self.m_panelMain, wx.ID_ANY, u"Input files"), wx.VERTICAL)
        m_listBoxInputfileChoices = []
        self.m_listBoxInputfile = wx.ListBox(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(150, -1),
                                             m_listBoxInputfileChoices, wx.LB_SINGLE | wx.HSCROLL)
        sbSizer3.Add(self.m_listBoxInputfile, 1, wx.ALL | wx.EXPAND, 5)
        bSizerListbox.Add(sbSizer3, 1, wx.ALL | wx.EXPAND, 10)
        bSizerSplitHor.Add(bSizerListbox, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)
        bSizerView = wx.BoxSizer(wx.VERTICAL)
        bSizerProgBar = wx.BoxSizer(wx.HORIZONTAL)

        self.GaugeBar = wx.Gauge(self.m_panelMain, wx.ID_ANY, 20, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.GaugeBar.SetValue(0)
        self.GaugeBar.SetMinSize(wx.Size(-1, 40))
        bSizerProgBar.Add(self.GaugeBar, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        bSizerView.Add(bSizerProgBar, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        bSizerViewHor = wx.BoxSizer(wx.VERTICAL)
        self.OkButton = wx.Button(self.m_panelMain, wx.ID_ANY, u"Process", wx.DefaultPosition, wx.Size(-1, -1), 0)
        bSizerViewHor.Add(self.OkButton, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)
        bSizerView.Add(bSizerViewHor, 1, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER | wx.ALL, 20)
        bSizerViewHor1 = wx.BoxSizer(wx.VERTICAL)

        self.CancelButton = wx.Button(self.m_panelMain, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size(-1, -1), 0)
        bSizerViewHor1.Add(self.CancelButton, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_LEFT | wx.ALL, 0)
        bSizerView.Add(bSizerViewHor1, 1, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER | wx.ALL, 20)
        bSizerSplitHor.Add(bSizerView, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        bSizerListbox_Output = wx.BoxSizer(wx.HORIZONTAL)
        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.m_panelMain, wx.ID_ANY, u"Output files"), wx.VERTICAL)
        m_listBoxOutputfileChoices = []
        self.m_listBoxOutputfile = wx.ListBox(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(150, -1),
                                              m_listBoxOutputfileChoices, wx.LB_SINGLE | wx.HSCROLL)
        sbSizer2.Add(self.m_listBoxOutputfile, 1, wx.ALL | wx.EXPAND, 5)

        bSizerListbox_Output.Add(sbSizer2, 1, wx.ALL | wx.EXPAND, 10)
        bSizerSplitHor.Add(bSizerListbox_Output, 1, wx.ALL | wx.EXPAND, 5)
        bSizerSplit.Add(bSizerSplitHor, 1, wx.EXPAND, 0)
        bSizerPanelMain.Add(bSizerSplit, 5, wx.EXPAND, 0)
        bSizerPanel.Add(bSizerPanelMain, 1, wx.EXPAND, 0)
        self.m_panelMain.SetSizer(bSizerPanel)
        self.m_panelMain.Layout()
        bSizerFrame.Add(self.m_panelMain, 1, wx.EXPAND, 0)
        self.SetSizer(bSizerFrame)
        self.Layout()

        self.Centre(wx.BOTH)
        self.dirPicker1.Bind(wx.EVT_DIRPICKER_CHANGED, self.dirPickerOnDirChanged)
        self.m_listBoxInputfile.Bind(wx.EVT_LISTBOX, self.m_listBoxInputfileOnListBox)
        self.m_listBoxInputfile.Bind(wx.EVT_LISTBOX_DCLICK, self.m_listBoxInputfileOnListBoxDClick)
        self.m_listBoxInputfile.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleClick_ListBox_Inputfile)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OkButtonOnButtonClick)
        self.OkButton.Bind(wx.EVT_LEFT_DCLICK, self.OkButtonOnLeftDClick)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.CancelButtonOnButtonClick)
        self.m_listBoxOutputfile.Bind(wx.EVT_LISTBOX, self.m_listBoxOutputfileOnListBox)
        self.m_listBoxOutputfile.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleClick_ListBox_Outputfile)
        self.Inputfilepath = ''

    def __del__(self):
        pass

    def dirPickerOnDirChanged(self, event):
        self.Inputfilepath = event.GetPath()
        self.GenerateInputfileList()
        file_path = self.Inputfilepath
        self.m_listBoxOutputfile.Clear()
        return file_path

    # pop input file list
    def GenerateInputfileList(self):
        self.m_listBoxInputfile.Clear()
        allFiles = os.listdir(self.Inputfilepath)
        chosen_file_path = self.Inputfilepath
        excel_pdf_allFiles = []
        for file in allFiles:
            if file.endswith('.PDF') or file.endswith('.pdf'):
                self.m_listBoxInputfile.Append(file)
                excel_pdf_allFiles.append(file)
        return excel_pdf_allFiles, chosen_file_path

    def m_listBoxInputfileOnListBoxDClick(self, event):
        event.Skip()

    def m_listBoxInputfileOnListBox(self, event):
        event.Skip()

    # double click to open the file using default tool
    def OnDoubleClick_ListBox_Inputfile(self, event):
        file_list, picked_file_path = self.GenerateInputfileList()
        file_selection = event.GetString()
        full_file_path = os.path.join(picked_file_path, file_selection)
        os.startfile(full_file_path, 'open')

    def OkButtonOnButtonClick(self, event):
        self.count = 0
        self.GaugeBar.SetValue(0)
        file_list, picked_file_path = self.GenerateInputfileList()
        os.chdir(picked_file_path)
        total_file_num = 0
        self.m_listBoxOutputfile.Clear()
        for file in file_list:
            if file.endswith('.pdf') or file.endswith('.PDF'):
                total_file_num += 1
        print(f'{date_time} - Info - Selected file path: : \n {picked_file_path} \n')

        print(f'{date_time} - Info - Selected {total_file_num} file(s): : \n {file_list} \n')

        self.GaugeBar.SetRange(total_file_num)
        file_flag = 0
        for file in file_list:
            if file.endswith('.pdf') or file.endswith('.PDF'):
                print(f'{date_time} - Info - Start processing file:  {file}\n')

                full_file_path = os.path.join(picked_file_path, file)
                if file_flag <3:
                    file_flag += 1
                main_func(picked_file_path, file)
                print(f'{date_time} - Info - Completed processing file:  {file} \n\n')

                self.count = self.count + 1
                self.GaugeBar.SetValue(self.count)

        all_file = os.listdir(picked_file_path)
        for file in all_file:
            if file.endswith('.xlsx'):
                self.m_listBoxOutputfile.Append(file)
        os.chdir(picked_file_path)

    # try this for progress bar
    def OkButtonOnLeftDClick(self, event):
         event.Skip()

    def CancelButtonOnButtonClick(self, event):
        self.Destroy()

    def m_listBoxOutputfileOnListBox(self, event):
        event.Skip()

    # double click to open the file using default tool
    def OnDoubleClick_ListBox_Outputfile(self, event):
        file_list, picked_file_path = self.GenerateInputfileList()
        file_selection = event.GetString()
        full_file_path = os.path.join(picked_file_path, file_selection)
        os.startfile(full_file_path, 'open')

class MainAPP(wx.App):
    def OnInit(self):
        mainFrame = frameMain(None)
        mainFrame.Show(True)
        return True

if __name__ == '__main__':
    # debugs multiple output window problem
    multiprocessing.freeze_support()
    if check_ey_pc():
        app = MainAPP()
        app.MainLoop()
