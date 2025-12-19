import os
import httpx

from mcp.server.fastmcp import FastMCP

# Brickognize API configuration
url = "https://api.brickognize.com/internal/search/"
params = {"external_catalogs": "bricklink", "predict_color": "true"}
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

# Initialize the MCP server
server = FastMCP("brick-finder")


def process_content(content: dict) -> dict:
    """
    Process the raw json response and format it into a readable text summary.
    Args:
        content (dict): The JSON response from Brickognize API containing detected_items
                        with candidate brick matches and their metadata.
    Returns:
        str: A formatted text summary of the brick identification results, including
            candidate names, probability scores, image URLs, BrickLink URLs, and
            predicted colors. Returns a "No candidates found" message if no matches.
    """
    candidates = []
    
    for item in content.get('detected_items', []):
        for candidate in item.get('candidate_items', []):
            candidate_info = {
                "name": candidate.get('name'),
                "score": candidate.get('score'),
                "image_url": candidate.get('image_url'),
                "bricklink_url": None,
                "top_color": None
            }
            
            # Get Bricklink URL if available
            external_items = candidate.get('external_items')
            if isinstance(external_items, list) and len(external_items):
                candidate_info["bricklink_url"] = external_items[0].get('url')
            
            # Get top candidate color if available
            candidate_colors = candidate.get('candidate_colors')
            if candidate_colors and isinstance(candidate_colors, list) and candidate_colors:
                top_color = candidate_colors[0]
                candidate_info["top_color"] = {
                    "name": top_color.get('name'),
                    "score": top_color.get('score')
                }

            candidates.append(candidate_info)
    
    result = {
        "success": True,
        "candidates": candidates,
        "count": len(candidates)
    }
    return result


@server.tool()
async def find_brick(file_path: str="") -> dict:
    """
    Search and identify LEGO bricks from an uploaded image given from file path.

    Returns json result of the brick identification results, including
    candidate names, probability scores, image URLs, BrickLink URLs, and
    predicted colors.
    """
    if file_path == "":
        raise ValueError("file_path is required")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")
        
        # Check file extension
        filename = os.path.basename(file_path)
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        
        if ext not in ['jpg', 'jpeg', 'png']:
            raise ValueError("Only PNG and JPEG images are supported")

        # Read image file
        with open(file_path, 'rb') as img:
            files = {'query_image': img}

            # Upload image file to Brickognize API using HTTP multipart encoding
            async with httpx.AsyncClient() as client:
                response = await client.post(url, files=files, headers=headers, params=params)
                response.raise_for_status()
                result = process_content(response.json())
                return result
        
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except PermissionError:
        raise ValueError(f"Permission denied accessing file: {file_path}")
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")


if __name__ == "__main__":
    # Run the server using stdio transport
    server.run(transport="stdio")
