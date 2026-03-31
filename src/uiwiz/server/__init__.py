from uiwiz.server._server import Config, Server


def run(app: str, host: str = "localhost", port: int = 8080) -> None:
    config = Config(host=host, port=port, app=app, root_path="")

    server = Server(config)
    server.run()
