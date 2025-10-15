import time
import requests
from typing import Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SunoApiToolSchema(BaseModel):
    """Input for SunoApiTool"""
    lyrics: str = Field(..., description="The lyrics for the song")


class SunoApiTool(BaseTool):
    name: str = "Generate a song with vocals from lyrics"
    description: str = (
        "A tool that generates a song with vocals from provided lyrics using Suno API. "
        "Pass the lyrics and the tool will generate a professional song."
    )
    args_schema: Type[BaseModel] = SunoApiToolSchema
    api_key: str = ""
    genre: str = ""
    base_url: str = "https://api.sunoapi.org/api/v1"
    
    def __init__(self, api_key: str, genre: str = "Pop", **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key
        self.genre = genre
    
    def _generate_song(self, lyrics: str) -> str:
        """Start song generation and return task ID"""
        url = f"{self.base_url}/generate"
        
        payload = {
            "prompt": lyrics,
            "style": self.genre,
            "title": "Melody Agents Song",
            "customMode": True,
            "instrumental": False,
            "model": "V3_5",
            "callBackUrl": "https://example.com/callback"  # Required but unused 
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 200:
                raise Exception(f"API Error: {result.get('msg', 'Unknown error')}")
            
            return result["data"]["taskId"]
        except Exception as e:
            raise Exception(f"Failed to start song generation: {str(e)}")
    
    def _poll_for_completion(self, task_id: str, max_wait: int = 300) -> dict:
        """Poll the API until song generation is complete"""
        url = f"{self.base_url}/generate/record-info"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        start_time = time.time()
        last_status = ""
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    url, 
                    params={"taskId": task_id},
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("code") != 200:
                    raise Exception(f"API Error: {result.get('msg', 'Unknown error')}")
                
                data = result["data"]
                status = data.get("status", "UNKNOWN")
                
                # Log status changes
                if status != last_status:
                    print(f"🎵 Status: {status}")
                    last_status = status
                
                # Check if completed
                if status == "SUCCESS":
                    return data
                elif "FAILED" in status or "ERROR" in status:
                    error_msg = data.get("errorMessage", "Unknown error")
                    raise Exception(f"Generation failed: {error_msg}")
                
                
                time.sleep(10)
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Polling error: {e}. Retrying...")
                time.sleep(10)
        
        raise Exception(f"Timeout: Song generation took longer than {max_wait}s")
    
    def _run(self, lyrics: str, **kwargs: Any) -> Any:
        """Generate a song using Suno API"""
        try:
            print(f"🎸 Genre: {self.genre}")
            print(f"📝 Lyrics: {len(lyrics)} characters")
            print("🚀 Starting song generation...")
            
            # Start generation
            task_id = self._generate_song(lyrics)
            print(f"✅ Task created: {task_id}")
            print("⏳ Waiting for completion (this may take 1-3 minutes)...")
            
            # Poll for completion
            result = self._poll_for_completion(task_id)
            
            # Extract song URLs
            suno_data = result.get("response", {}).get("sunoData", [])
            
            if not suno_data:
                return "❌ No songs were generated"
            
            output = "🎉 Song Generated Successfully! 🎵\n\n"
            output += f"**Genre:** {self.genre}\n"
            output += f"**Task ID:** {task_id}\n\n"
            output += "**Download Your Song(s):**\n"
            
            for i, song in enumerate(suno_data, 1):
                output += f"\n**Song {i}:**\n"
                output += f"- Title: {song.get('title', 'Melody Agents Song')}\n"
                output += f"- Duration: {song.get('duration', 0):.2f}s\n"
                output += f"- Audio URL: {song.get('audioUrl', 'N/A')}\n"
                output += f"- Cover Image: {song.get('imageUrl', 'N/A')}\n"
            
            output += "\n⚠️ **Note:** URLs may expire after some time. Download soon!\n"
            
            return output
            
        except Exception as e:
            return f"❌ Error generating song: {str(e)}"