# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict

import click

from lean.components.util.logger import Logger
from lean.models.brokerages.local.base import LeanConfigConfigurer, LocalBrokerage


class BinanceBrokerage(LocalBrokerage):
    """A LocalBrokerage implementation for the Binance brokerage."""

    @classmethod
    def get_name(cls) -> str:
        return "Binance"

    @classmethod
    def _configure_environment(cls, lean_config: Dict[str, Any], environment_name: str) -> None:
        lean_config["environments"][environment_name]["live-mode-brokerage"] = "BinanceBrokerage"
        lean_config["environments"][environment_name]["transaction-handler"] = \
            "QuantConnect.Lean.Engine.TransactionHandlers.BrokerageTransactionHandler"

    @classmethod
    def _configure_credentials(cls, lean_config: Dict[str, Any], logger: Logger) -> None:
        logger.info("""
Create an API key by logging in and accessing the Binance API Management page (https://www.binance.com/en/my/settings/api-management).
        """.strip())

        lean_config["binance-api-key"] = click.prompt("API key", cls._get_default(lean_config, "binance-api-key"))
        lean_config["binance-api-secret"] = logger.prompt_password("API secret",
                                                                   cls._get_default(lean_config, "binance-api-secret"))

        cls._save_properties(lean_config, ["binance-api-key", "binance-api-secret"])


class BinanceDataFeed(LeanConfigConfigurer):
    """A LeanConfigConfigurer implementation for the Binance data feed."""

    @classmethod
    def get_name(cls) -> str:
        return BinanceBrokerage.get_name()

    @classmethod
    def configure(cls, lean_config: Dict[str, Any], environment_name: str, logger: Logger) -> None:
        lean_config["environments"][environment_name]["data-queue-handler"] = "BinanceBrokerage"
        lean_config["environments"][environment_name]["history-provider"] = "BrokerageHistoryProvider"

        BinanceBrokerage.configure_credentials(lean_config, logger)
