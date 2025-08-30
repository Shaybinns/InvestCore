# Memory package for InvestCore AI
# This file makes the memory directory a Python package

from .short_term_cache import (
    get_recent_conversation,
    add_to_recent_conversation,
    update_current_cache,
    get_current_cache,
    update_market_data,
    get_current_market_data,
    get_comprehensive_cache,
    get_user_data_summary
)

from .command_stack import (
    push_stack,
    peek_stack,
    pop_stack,
    mark_current_complete,
    start_command_execution,
    has_pending_steps,
    get_stack_state,
    get_current_goal,
    get_stack_summary,
    clear_completed_stack
)

from .running_state import (
    set_running,
    is_running,
    get_running_context,
    update_running_context,
    pause_execution,
    resume_execution,
    get_execution_summary,
    log_session_event
)

__all__ = [
    # Short term cache functions
    'get_recent_conversation',
    'add_to_recent_conversation', 
    'update_current_cache',
    'get_current_cache',
    'update_market_data',
    'get_current_market_data',
    'get_comprehensive_cache',
    'get_user_data_summary',
    
    # Command stack functions
    'push_stack',
    'peek_stack',
    'pop_stack',
    'mark_current_complete',
    'start_command_execution',
    'has_pending_steps',
    'get_stack_state',
    'get_current_goal',
    'get_stack_summary',
    'clear_completed_stack',
    
    # Running state functions
    'set_running',
    'is_running',
    'get_running_context',
    'update_running_context',
    'pause_execution',
    'resume_execution',
    'get_execution_summary',
    'log_session_event'
]
