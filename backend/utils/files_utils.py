
import os

# Files to exclude from operations
EXCLUDED_FILES = {
    ".DS_Store",
    ".gitignore",
    "package-lock.json",
    "postcss.config.js",
    "postcss.config.mjs",
    "jsconfig.json",
    "components.json",
    "tsconfig.tsbuildinfo",
    "tsconfig.json",
}

# Directories to exclude from operations
EXCLUDED_DIRS = {
    "node_modules",
    ".next",
    "dist",
    "build",
    ".git"
}

# File extensions to exclude from operations
EXCLUDED_EXT = {
    ".ico",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".webp",
    ".db",
    ".sql"
}

def should_exclude_file(rel_path: str) -> bool:
    """Check if a file should be excluded based on path, name, or extension
    
    Args:
        rel_path: Relative path of the file to check
        
    Returns:
        True if the file should be excluded, False otherwise
    """
    # Check filename
    filename = os.path.basename(rel_path)
    if filename in EXCLUDED_FILES:
        return True

    # Check directory
    dir_path = os.path.dirname(rel_path)
    if any(excluded in dir_path for excluded in EXCLUDED_DIRS):
        return True

    # Check extension
    _, ext = os.path.splitext(filename)
    if ext.lower() in EXCLUDED_EXT:
        return True

    return False 

def clean_path(path: str, workspace_path: str = "/workspace") -> str:
    """Clean and normalize a path to be relative to the workspace
    
    Args:
        path: The path to clean
        workspace_path: The base workspace path to remove (default: "/workspace")
        
    Returns:
        The cleaned path, relative to the workspace
    """
    # Remove any leading slash
    path = path.lstrip('/')
    
    # Remove workspace prefix if present
    if path.startswith(workspace_path.lstrip('/')):
        path = path[len(workspace_path.lstrip('/')):]
    
    # Remove workspace/ prefix if present
    if path.startswith('workspace/'):
        path = path[9:]
    
    # Remove any remaining leading slash
    path = path.lstrip('/')
    
    return path 

def enforce_workspace_path(path: str, workspace_path: str = "/workspace") -> str:
    """Enforce that a path is within the workspace directory and normalize it
    
    This function provides stronger validation than clean_path to prevent
    directory traversal attacks and ensure agents always work within /workspace.
    
    Args:
        path: The path to validate and normalize
        workspace_path: The base workspace path (default: "/workspace")
        
    Returns:
        The validated and normalized path within the workspace
        
    Raises:
        ValueError: If the path attempts to access files outside the workspace
    """
    import os
    
    # Check for absolute paths that don't start with workspace_path
    if os.path.isabs(path) and not path.startswith(workspace_path):
        # Log the security violation if logger is available
        try:
            from utils.logger import logger
            logger.warning(f"Agent attempted to access absolute path outside workspace: {path}")
        except ImportError:
            pass
        raise ValueError(f"Absolute path '{path}' is outside the allowed workspace directory. All files must be within {workspace_path}")
    
    # Clean the input path first
    cleaned_path = clean_path(path, workspace_path)
    
    # Build the full path
    full_path = os.path.join(workspace_path, cleaned_path)
    
    # Normalize to resolve any .. or . components
    normalized_path = os.path.normpath(full_path)
    
    # Ensure the path is still within the workspace
    if not normalized_path.startswith(workspace_path):
        # Log the security violation if logger is available
        try:
            from utils.logger import logger
            logger.warning(f"Agent attempted to access path outside workspace: {path} -> {normalized_path}")
        except ImportError:
            pass
        raise ValueError(f"Path '{path}' resolves outside the allowed workspace directory. All files must be within {workspace_path}")
    
    # Return the relative path from workspace
    relative_path = os.path.relpath(normalized_path, workspace_path)
    
    # Handle the case where the path is exactly the workspace root
    if relative_path == '.':
        return ''
    
    return relative_path