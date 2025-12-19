# Brick Finder MCP Server

A Model Context Protocol (MCP) server that identifies LEGO brick parts from images using the Brickognize API.

## Background

This MCP server provides an AI assistant tool for identifying LEGO brick parts from uploaded images. It leverages the [Brickognize API](https://api.brickognize.com/) to analyze images and return detailed information about detected brick parts including:

- Brick names and part numbers
- Confidence scores for identification accuracy
- Thumbnail images of the identified parts
- BrickLink URLs for purchasing information
- Predicted brick colors with confidence scores

The server is built using the FastMCP framework and provides a single `find_brick` tool that can be used by MCP-compatible AI assistants like Claude Desktop.

## Features

- 🧱 **LEGO Brick Identification**: Upload images to identify specific LEGO parts
- 🎯 **High Accuracy**: Powered by Brickognize's machine learning models
- 🔗 **BrickLink Integration**: Get direct links to purchase identified parts
- 🎨 **Color Prediction**: Automatic color identification with confidence scores
- ⚡ **Async Support**: Built with modern async/await patterns for performance
- 🛠️ **MCP Compatible**: Works with any MCP-compatible AI assistant

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd brick_finder_mcp
   ```

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Run Locally
1. **Start the server**:
   ```bash
   python main.py
   ```

2. **Configure your MCP client** (e.g., Claude Desktop):
   
   Add the following to your MCP configuration:
   ```json
   {
     "mcpServers": {
       "brick-identifier": {
         "command": "python",
         "args": ["path/to/brick_finder_mcp/main.py"],
       }
     }
   }
   ```

3. **Use the tool**: Once connected, you can use the `find_brick` tool in your AI assistant by providing the path to an image file containing LEGO bricks.

## Usage

### Tool: `find_brick`

Identifies LEGO brick parts from an image file.

**Parameters:**
- `file_path` (string): Absolute path to the image file (PNG or JPEG)

**Example:**
```
Please identify the LEGO brick in this image: /path/to/your/brick_image.jpg
```

**Sample Output:**
```
### Brick Search Results ###

Candidate 1: Brick 1 x 4
  - probability: 0.956
  - image: https://cdn.brickognize.com/thumbnails/...
  - bricklink: https://www.bricklink.com/v2/catalog/catalogitem.page?P=3010
  - color: Red (score: 0.892)

Candidate 2: Brick 1 x 3
  - probability: 0.234
  - image: https://cdn.brickognize.com/thumbnails/...
  - bricklink: https://www.bricklink.com/v2/catalog/catalogitem.page?P=3622
  - color: Red (score: 0.756)
```

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## Project Structure

```
brick_finder_mcp/
├── main.py                # Main MCP server implementation
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Poetry configuration
├── plan.md               # Project planning notes
└── README.md             # This file
```

## Acknowledgments

- [Brickognize](https://brickognize.com/) for providing the brick identification API
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP framework
- [FastMCP](https://github.com/jlowin/fastmcp) for the server implementation