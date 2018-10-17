from sshtunnel import SSHTunnelForwarder
server = SSHTunnelForwarder(
    'multi.proxy.mediatube.xyz',
    ssh_username="proxyuser",
    ssh_password="8X5tjtV5ISNv2",
    remote_bind_address=('localhost', 433),
    ssh_port=2278
)