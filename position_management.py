import datetime
import logging
import threading
from typing import List

from models import Script, Position
from variables import *
from constants import *
from utils import write_file

# Global variables
logger = logging.getLogger("PositionsManager")


class PositionsManager:

    def __init__(self):
        pass

    @staticmethod
    def get_position(symbol) -> Position:
        return Position.get_position(symbol)

    @staticmethod
    def get_script(symbol) -> Script:
        return Script.get_script(symbol)

    @staticmethod
    def add_position(position: Position):
        positions_db[position.script.symbol] = position
        return positions_db[position.script.symbol]

    @staticmethod
    def get_archived_positions(symbol: str) -> List[Position]:
        return position_archives.get(symbol, [])

    @staticmethod
    def archive_position(position: Position):
        positions_db[position.script.symbol] = None
        positions = position_archives.get(position.script.symbol, [])
        positions.append(position)
        position_archives[position.script.symbol] = positions

    @staticmethod
    def update_script(script: Script) -> Script:
        return Script.add_or_update_script(script)

    @staticmethod
    def get_script_lock(symbol) -> threading.Lock:
        return script_locks[symbol]

    @staticmethod
    def get_or_create_script_lock(symbol) -> threading.Lock:
        if symbol not in script_locks:
            script_locks[symbol] = threading.Lock()
        return script_locks[symbol]

    @staticmethod
    def print_summary():
        now = datetime.datetime.now()
        total_gross_pnl = 0
        total_charges = 0
        total_positive = 0
        total_negative = 0

        ce_entries = 0
        pe_entries = 0
        ce_exits = 0
        pe_exits = 0
        ce_positive = 0
        pe_positive = 0
        ce_negative = 0
        pe_negative = 0

        gross_pnl = 0
        charges = 0

        logger.info("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        logger.info(now.strftime("%Y-%m-%d") + " Summary: \n\n\n")
        logger.info("REGULAR ENTRY:")
        for positions in position_archives.values():
            for position in positions:
                if position.strategy.value == Strategy.REGULAR.value:
                    if position.script.option_type.value == OptionType.CE.value:
                        ce_entries += 1
                        if position.exit_reason != "Square Off":
                            ce_exits += 1
                        if position.gross_pnl >= 0:
                            ce_positive += 1
                        else:
                            ce_negative += 1
                    else:
                        pe_entries += 1
                        if position.exit_reason != "Square Off":
                            pe_exits += 1

                        if position.gross_pnl >= 0:
                            pe_positive += 1
                        else:
                            pe_negative += 1

                    gross_pnl += position.gross_pnl
                    charges += position.charges
        logger.info(f"Total trades: {ce_entries + pe_entries}")
        logger.info(f"Total CE Entries: {ce_entries}, Exits: {ce_exits}, SquareOff: {ce_entries - ce_exits}")
        logger.info(f"Total PE Entries: {pe_entries}, Exits: {pe_exits}, SquareOff: {pe_entries - pe_exits}")
        logger.info(f"Total CE Positive trades: {ce_positive}, CE Negative trades: {ce_negative}")
        logger.info(f"Total PE Positive trades: {pe_positive}, PE Negative trades: {pe_negative}")
        logger.info(f"Gross PnL: {gross_pnl}, Charges: {charges}, Net PnL: {gross_pnl - charges}")
        total_gross_pnl += gross_pnl
        total_charges += charges
        total_positive += ce_positive + pe_positive
        total_negative += ce_negative + pe_negative

        ce_entries = 0
        pe_entries = 0
        ce_exits = 0
        pe_exits = 0
        ce_positive = 0
        pe_positive = 0
        ce_negative = 0
        pe_negative = 0

        gross_pnl = 0
        charges = 0
        logger.info("\n\n\n\n\n\n\n\n")
        logger.info("REVISED 1 ENTRY:")
        for positions in position_archives.values():
            for position in positions:
                if position.strategy.value == Strategy.REVISED_1.value:
                    if position.script.option_type.value == OptionType.CE.value:
                        ce_entries += 1
                        if position.exit_reason != "Square Off":
                            ce_exits += 1
                        if position.gross_pnl >= 0:
                            ce_positive += 1
                        else:
                            ce_negative += 1
                    else:
                        pe_entries += 1
                        if position.exit_reason != "Square Off":
                            pe_exits += 1

                        if position.gross_pnl >= 0:
                            pe_positive += 1
                        else:
                            pe_negative += 1

                    gross_pnl += position.gross_pnl
                    charges += position.charges
        logger.info(f"Total trades: {ce_entries + pe_entries}")
        logger.info(f"Total CE Entries: {ce_entries}, Exits: {ce_exits}, SquareOff: {ce_entries - ce_exits}")
        logger.info(f"Total PE Entries: {pe_entries}, Exits: {pe_exits}, SquareOff: {pe_entries - pe_exits}")
        logger.info(f"Total CE Positive trades: {ce_positive}, CE Negative trades: {ce_negative}")
        logger.info(f"Total PE Positive trades: {pe_positive}, PE Negative trades: {pe_negative}")
        logger.info(f"Gross PnL: {gross_pnl}, Charges: {charges}, Net PnL: {gross_pnl - charges}")
        total_gross_pnl += gross_pnl
        total_charges += charges
        total_positive += ce_positive + pe_positive
        total_negative += ce_negative + pe_negative

        ce_entries = 0
        pe_entries = 0
        ce_exits = 0
        pe_exits = 0
        ce_positive = 0
        pe_positive = 0
        ce_negative = 0
        pe_negative = 0

        gross_pnl = 0
        charges = 0
        logger.info("\n\n\n\n\n\n\n\n")
        logger.info("REVISED 2 ENTRY:")
        for positions in position_archives.values():
            for position in positions:
                if position.strategy.value == Strategy.REVISED_2.value:
                    if position.script.option_type.value == OptionType.CE.value:
                        ce_entries += 1
                        if position.exit_reason != "Square Off":
                            ce_exits += 1
                        if position.gross_pnl >= 0:
                            ce_positive += 1
                        else:
                            ce_negative += 1
                    else:
                        pe_entries += 1
                        if position.exit_reason != "Square Off":
                            pe_exits += 1

                        if position.gross_pnl >= 0:
                            pe_positive += 1
                        else:
                            pe_negative += 1

                    gross_pnl += position.gross_pnl
                    charges += position.charges
        logger.info(f"Total trades: {ce_entries + pe_entries}")
        logger.info(f"Total CE Entries: {ce_entries}, Exits: {ce_exits}, SquareOff: {ce_entries - ce_exits}")
        logger.info(f"Total PE Entries: {pe_entries}, Exits: {pe_exits}, SquareOff: {pe_entries - pe_exits}")
        logger.info(f"Total CE Positive trades: {ce_positive}, CE Negative trades: {ce_negative}")
        logger.info(f"Total PE Positive trades: {pe_positive}, PE Negative trades: {pe_negative}")
        logger.info(f"Gross PnL: {gross_pnl}, Charges: {charges}, Net PnL: {gross_pnl - charges}")
        total_gross_pnl += gross_pnl
        total_charges += charges
        total_positive += ce_positive + pe_positive
        total_negative += ce_negative + pe_negative

        ce_entries = 0
        pe_entries = 0
        ce_exits = 0
        pe_exits = 0
        ce_positive = 0
        pe_positive = 0
        ce_negative = 0
        pe_negative = 0

        gross_pnl = 0
        charges = 0
        logger.info("\n\n\n\n\n\n\n\n")
        logger.info("GAP ENTRY:")
        for positions in position_archives.values():
            for position in positions:
                if position.strategy.value == Strategy.GAP.value:
                    if position.script.option_type.value == OptionType.CE.value:
                        ce_entries += 1
                        if position.exit_reason != "Square Off":
                            ce_exits += 1
                        if position.gross_pnl >= 0:
                            ce_positive += 1
                        else:
                            ce_negative += 1
                    else:
                        pe_entries += 1
                        if position.exit_reason != "Square Off":
                            pe_exits += 1

                        if position.gross_pnl >= 0:
                            pe_positive += 1
                        else:
                            pe_negative += 1

                    gross_pnl += position.gross_pnl
                    charges += position.charges
        logger.info(f"Total trades: {ce_entries + pe_entries}")
        logger.info(f"Total CE Entries: {ce_entries}, Exits: {ce_exits}, SquareOff: {ce_entries - ce_exits}")
        logger.info(f"Total PE Entries: {pe_entries}, Exits: {pe_exits}, SquareOff: {pe_entries - pe_exits}")
        logger.info(f"Total CE Positive trades: {ce_positive}, CE Negative trades: {ce_negative}")
        logger.info(f"Total PE Positive trades: {pe_positive}, PE Negative trades: {pe_negative}")
        logger.info(f"Gross PnL: {gross_pnl}, Charges: {charges}, Net PnL: {gross_pnl - charges}")
        total_gross_pnl += gross_pnl
        total_charges += charges
        total_positive += ce_positive + pe_positive
        total_negative += ce_negative + pe_negative

        logger.info("\n\n\n" + now.strftime("%Y-%m-%d") + " FINAL SUMMARY: ")
        logger.info(f"Gross PnL: {total_gross_pnl}, Charges: {total_charges}, "
                    f"Net PnL: {total_gross_pnl - total_charges}, Positive trades: {total_positive}, "
                    f"Negative trades: {total_negative}, Total margin used: {margin.max}\n\n\n\n\n\n\n\n")

    @staticmethod
    def save_db():
        file_name = datetime.datetime.now().strftime("resources/positions_data/positions_data-%Y-%m-%d.pickle")
        write_file(position_archives, file_name)
        logger.info(f"Write DB file: {file_name} to disk")
