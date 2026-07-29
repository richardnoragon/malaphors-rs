import json
import random
import tkinter.messagebox
import re
from functools import lru_cache
from pathlib import Path
import asyncio
import logging
from typing import List, Dict, Optional, Tuple

class MalaphorGenerator:
    """Generate and manage malaphors from combinations of phrases."""
    
    def __init__(self):
        """Initialize the MalaphorGenerator with phrases from JSON file."""
        self.proverbs = []
        self.history = []
        self.favorites = []
        self.logger = logging.getLogger('malaphor_logger')
        self._load_data()
        
    def _load_data(self) -> None:
        """Load malaphors and favorites from JSON files."""
        try:
            self._load_malaphors()
            self._load_favorites()
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
            
    def _load_malaphors(self) -> None:
        """Load malaphors from the JSON file."""
        try:
            with open("malaphors.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                self.proverbs = data["proverbs"]
        except FileNotFoundError:
            self.logger.error("malaphors.json file not found!")
            raise
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON format in malaphors.json!")
            raise

    def _load_favorites(self) -> None:
        """Load favorites from the JSON file."""
        try:
            with open("favorites.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                self.favorites = data.get("favorites", [])
        except (FileNotFoundError, json.JSONDecodeError):
            # It's okay if the file doesn't exist yet
            pass

    @lru_cache(maxsize=128)
    def _get_split_points(self, phrase: str) -> Tuple[str, str]:
        """Cache split points for phrases to avoid recomputing."""
        return self.smart_split_phrase(phrase)

    def smart_split_phrase(self, phrase: str) -> Tuple[str, str]:
        """Split a phrase into beginning and ending parts."""
        # Special case for 'but' since it should start the second part
        if ", but " in phrase:
            parts = phrase.split(", but ", 1)
            return parts[0].strip(), "but " + parts[1].strip()
        elif " but " in phrase:
            parts = phrase.split(" but ", 1)
            return parts[0].strip(), "but " + parts[1].strip()
            
        # Special case for "Actions speak louder than words" pattern
        parts = phrase.split(" speak ", 1)
        if len(parts) == 2 and parts[0].strip() == "Actions":
            return "Actions", "speak " + parts[1].strip()
            
        # Other common delimiters
        delimiters = [', and ', ' and ', ', ', '; ', ': ']
        for delimiter in delimiters:
            if delimiter in phrase:
                parts = phrase.split(delimiter, 1)
                return parts[0].strip(), parts[1].strip()
        
        # If no delimiter found, split at closest word to middle
        words = phrase.split()
        mid = len(words) // 2
        return ' '.join(words[:mid]), ' '.join(words[mid:])

    async def _save_to_file(self, filepath: str, data: dict) -> bool:
        """Asynchronously save data to a JSON file."""
        try:
            # Create parent directories if they don't exist
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Write data asynchronously using asyncio
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: Path(filepath).write_text(
                    json.dumps(data, indent=2),
                    encoding='utf-8'
                )
            )
            return True
        except Exception as e:
            self.logger.error(f"Error saving to {filepath}: {str(e)}")
            return False

    def generate_malaphor(self, source1_index: Optional[int] = None, source2_index: Optional[int] = None) -> Dict[str, str]:
        """Generate a malaphor by combining parts of two phrases."""
        if len(self.proverbs) < 2:
            raise ValueError("Not enough proverbs to generate a malaphor")
            
        while True:
            proverb1 = self.proverbs[source1_index] if source1_index is not None else random.choice(self.proverbs)
            proverb2 = self.proverbs[source2_index] if source2_index is not None else random.choice(self.proverbs)
            
            if source1_index is not None and source2_index is not None:
                break
                
            if proverb2 != proverb1:  # Avoid same-phrase combinations
                break
        
        new_malaphor = f"{proverb1['beginning']} {proverb2['ending']}"
        
        result = {
            "malaphor": new_malaphor,
            "source1": proverb1["original"],
            "source2": proverb2["original"]
        }
        
        self.history.append(result)
        return result

    async def add_new_proverb(self, phrase_or_beginning: str, ending: str = None) -> bool:
        """Add a new proverb to the collection."""
        try:
            if ending:
                beginning = phrase_or_beginning
            else:
                beginning, ending = self._get_split_points(phrase_or_beginning)
                
            new_proverb = {
                "original": f"{beginning} {ending}",
                "beginning": beginning,
                "ending": ending
            }
            
            self.proverbs.append(new_proverb)
            return await self._save_to_file("malaphors.json", {"proverbs": self.proverbs})
        except Exception as e:
            self.logger.error(f"Error adding new proverb: {str(e)}")
            return False

    def add_to_favorites(self, malaphor: str) -> None:
        """Add a malaphor to favorites."""
        if malaphor not in self.favorites:
            self.favorites.append(malaphor)
            self.save_favorites()

    async def save_favorites(self) -> None:
        """Save favorite malaphors to a JSON file."""
        await self._save_to_file("favorites.json", {"favorites": self.favorites})

    async def export_malaphors(self, filepath: str) -> bool:
        """Export all original malaphors to a JSON file."""
        return await self._save_to_file(filepath, {"proverbs": self.proverbs})

    async def export_history(self, filepath: str) -> bool:
        """Export generated malaphor history to a JSON file."""
        return await self._save_to_file(filepath, {"history": self.history})

    async def export_malaphors_as_text(self, filepath: str) -> bool:
        """Export all original malaphors to a text file."""
        try:
            text = '\n'.join(proverb['original'] for proverb in self.proverbs)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: Path(filepath).write_text(text, encoding='utf-8')
            )
            return True
        except Exception as e:
            self.logger.error(f"Error exporting malaphors as text: {str(e)}")
            return False

    async def export_history_as_text(self, filepath: str) -> bool:
        """Export generated malaphor history to a text file."""
        try:
            lines = []
            for item in self.history:
                lines.extend([
                    f"Malaphor: {item['malaphor']}",
                    f"Created from:",
                    f"1. {item['source1']}",
                    f"2. {item['source2']}\n"
                ])
            text = '\n'.join(lines)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: Path(filepath).write_text(text, encoding='utf-8')
            )
            return True
        except Exception as e:
            self.logger.error(f"Error exporting history as text: {str(e)}")
            return False

    async def export_favorites_as_text(self, filepath: str) -> bool:
        """Export favorites to a text file."""
        try:
            text = '\n\n'.join(self.favorites)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: Path(filepath).write_text(text, encoding='utf-8')
            )
            return True
        except Exception as e:
            self.logger.error(f"Error exporting favorites as text: {str(e)}")
            return False

    async def import_malaphors(self, filepath: str) -> bool:
        """Import malaphors from a JSON file and merge with existing ones."""
        try:
            content = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: Path(filepath).read_text(encoding='utf-8')
            )
            data = json.loads(content)
            
            if "proverbs" in data:
                # Create a set of existing originals to avoid duplicates
                existing = {p["original"] for p in self.proverbs}
                new_proverbs = []
                skipped_proverbs = []
                
                for proverb in data["proverbs"]:
                    if proverb["original"] not in existing:
                        new_proverbs.append(proverb)
                    else:
                        skipped_proverbs.append(proverb["original"])
                
                if new_proverbs:
                    self.proverbs.extend(new_proverbs)
                    # Save the merged proverbs
                    if await self._save_to_file("malaphors.json", {"proverbs": self.proverbs}):
                        message = f"Successfully imported {len(new_proverbs)} new malaphors!"
                        if skipped_proverbs:
                            message += f"\n\nSkipped {len(skipped_proverbs)} duplicates."
                        self.logger.info(message)
                        return True
                else:
                    message = f"No new malaphors to import.\n{len(skipped_proverbs)} duplicates were found."
                    self.logger.info(message)
                    return False
            return False
        except Exception as e:
            self.logger.error(f"Error importing malaphors: {str(e)}")
            return False

    async def edit_proverb(self, index: int, beginning: str, ending: str) -> bool:
        """Edit an existing proverb and save changes to file."""
        if index < 0 or index >= len(self.proverbs):
            return False
            
        self.proverbs[index] = {
            "original": f"{beginning} {ending}",
            "beginning": beginning,
            "ending": ending
        }
        
        return await self._save_to_file("malaphors.json", {"proverbs": self.proverbs})

    async def delete_proverb(self, index: int) -> bool:
        """Delete a proverb and save changes to file."""
        if index < 0 or index >= len(self.proverbs):
            return False
            
        del self.proverbs[index]
        return await self._save_to_file("malaphors.json", {"proverbs": self.proverbs})

    def get_all_proverbs(self) -> List[Dict[str, str]]:
        """Return all proverbs."""
        return self.proverbs

    def delete_from_history(self, index: int) -> None:
        """Delete an item from history by index."""
        if 0 <= index < len(self.history):
            del self.history[index]

    def delete_from_favorites(self, index: int) -> None:
        """Delete an item from favorites by index."""
        if 0 <= index < len(self.favorites):
            del self.favorites[index]
            asyncio.create_task(self.save_favorites())

    @lru_cache(maxsize=32)
    def search_history(self, query: str) -> List[Tuple[int, Dict[str, str]]]:
        """Search history items for a query string."""
        query = query.lower()
        return [
            (i, item) for i, item in enumerate(self.history)
            if query in item["malaphor"].lower() or
               query in item["source1"].lower() or
               query in item["source2"].lower()
        ]

    @lru_cache(maxsize=32)
    def search_favorites(self, query: str) -> List[Tuple[int, str]]:
        """Search favorites for a query string."""
        query = query.lower()
        return [
            (i, item) for i, item in enumerate(self.favorites)
            if query in item.lower()
        ]