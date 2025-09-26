#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Payment API 启动脚本
"""

if __name__ == "__main__":
    import sys
    import os
    
    # 添加src目录到Python路径
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    import uvicorn
    from src.web_config import settings
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8077,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )