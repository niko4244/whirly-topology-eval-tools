FEATURE_FLAGS = {
    "new_doc_parser": True,
    "beta_training_ui": False
}

def is_enabled(flag):
    return FEATURE_FLAGS.get(flag, False)