def esta_em_venv():
    import sys
    import os
    
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get("VIRTUAL_ENV") is not None
    )
    