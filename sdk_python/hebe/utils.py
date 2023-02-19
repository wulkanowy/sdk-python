from aiohttp import ClientSession
from sdk_python.hebe.error import InvalidTokenException

ROUTING_RULES_URL: str = (
    "http://komponenty.vulcan.net.pl/UonetPlusMobile/RoutingRules.txt"
)


async def get_servers_list() -> dict[str, str]:
    session = ClientSession()
    servers_list_response = await session.get(ROUTING_RULES_URL)
    servers_list_text: str = await servers_list_response.text()
    servers_list: dict = {
        server.split(",")[0]: server.split(",")[1]
        for server in servers_list_text.split()
    }
    servers_list.update({"FK1": "http://api.fakelog.cf"})
    return servers_list


async def get_server_url_by_token(token: str) -> str:
    servers_list: dict[str, str] = await get_servers_list()
    try:
        return servers_list[token[:3]]
    except:
        raise InvalidTokenException()
