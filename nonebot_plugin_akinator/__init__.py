# ruff: noqa: E402

from nonebot import logger
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_waiter")
require("nonebot_plugin_alconna")

from .const import HTML_RENDER_AVAILABLE

if HTML_RENDER_AVAILABLE:
    require("nonebot_plugin_htmlrender")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel, config  # noqa: E402

__version__ = "1.0.3-trimo"
__plugin_meta__ = PluginMetadata(
    name="Akinator",
    description="网络天才",
    usage="使用 `akinator` 指令开始让我猜人物吧！",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-akinator",
    type="application",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_waiter",
        "nonebot_plugin_alconna",
    ),
    extra={"License": "MIT", "Author": "LgCookie"},
)


if config.akinator_client_type == "playwright":
    if not HTML_RENDER_AVAILABLE:
        logger.warning(
            "网络天才客户端类型目前为 playwright，但所需依赖并未安装。"
            "可以通过`pip install nonebot-plugin-akinator[image]`在安装本插件时自动安装对应依赖。"
            "现在，已回退至 HTTPX 客户端。\n"
            "另外：如果你想用 patchright 以绕过 Cloudflare 人机检测，"
            "可以执行`pip install nonebot-plugin-akinator[patchright]`来安装对应内容。"
            "然后执行`nb akinator-patch-import`以使之生效。",
        )
    else:
        from nonebot import get_driver
        from nonebot_plugin_htmlrender import init

        driver = get_driver()
        driver._lifespan._startup_funcs.remove(init)  # noqa: SLF001

        @driver.on_startup
        async def new_init():
            await init(headless=False)  # type: ignore
