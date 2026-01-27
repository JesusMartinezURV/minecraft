import asyncio
from src.utils.logging import Logger


async def main():
    """Test the Logger singleton"""
    
    # Get the singleton logger instance
    logger = Logger()
    
    print("=" * 60)
    print("Testing Logger Singleton")
    print("=" * 60)
    print()
    
    # Test 1: Basic info logging
    logger.log_info("MinerBot", "perceive", "Scanning environment for resources")
    
    # Test 2: Another info log
    logger.log_error("ExplorerBot", "navigate", "Moving to unexplored chunk")
    
    # Test 3: Another info log from same agent
    logger.log_debug("BuilderBot", "construct", "Building wooden house")
    
    # Simulate some async operations
    await asyncio.sleep(1)
    
    # Test 4: Verify singleton (same instance)
    logger2 = Logger()
    print()
    print(f"Same instance check: {logger is logger2}")  # Should be True
    
    await asyncio.sleep(1)
    
    # Test 5: More logs from different agents
    logger.log_info("MinerBot", "act", "Mining coal ore successfully")
    logger.log_info("ExplorerBot", "perceive", "Found new biome: Dark Forest")
    
    print()
    print("=" * 60)
    print(" Logging test complete!")
    print("Check app.log file for file output")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
