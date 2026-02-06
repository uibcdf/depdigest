PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": True,
    "capture_logging": True,
    "theme": "plain",
}

PROFILES = {
    "user": {
        "level": "WARNING",
    },
    "dev": {
        "level": "INFO",
        "show_traceback": True,
    },
    "qa": {
        "level": "INFO",
        "show_traceback": True,
    },
    "agent": {
        "level": "WARNING",
    },
    "debug": {
        "level": "DEBUG",
        "show_traceback": True,
    },
}

CODES = {
    "DEPDIGEST-MISSING-DEPENDENCY": {
        "title": "Missing dependency",
        "user_message": "La libreria '{library}' es necesaria y no esta instalada.",
        "user_hint": "Instala '{library}' (pip: {pip_install}, conda: {conda_install}).",
        "dev_message": "Missing dependency '{library}' required by '{caller}'.",
        "dev_hint": "Install via {pip_install} or {conda_install}.",
        "qa_message": "Missing dependency '{library}' required by '{caller}'.",
        "qa_hint": "Install via {pip_install} or {conda_install}.",
        "agent_message": "Missing dependency '{library}' required by '{caller}'.",
        "agent_hint": "Install via {pip_install} or {conda_install}.",
    }
}

SIGNALS = {
    "depdigest.check_dependency": {
        "extra_required": ["library", "caller", "pip_install", "conda_install"],
    }
}
