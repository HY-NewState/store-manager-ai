import threading

def debounce(wait):
    """데코레이터로 사용할 수 있는 debounce 함수 생성기"""
    def decorator(fn):
        # fn이 호출되면 새로운 스레드에서 실행되게 함
        timer = None
        
        def debounced(*args, **kwargs):
            nonlocal timer
            # 기존에 설정된 타이머가 있다면 취소
            if timer is not None:
                timer.cancel()
                
            # 새로운 타이머 설정
            def call_it():
                fn(*args, **kwargs)
                
            timer = threading.Timer(wait, call_it)
            timer.start()

        return debounced
    return decorator

# 사용 예
# @debounce(0.5)  # 0.5초 동안 추가 호출이 없으면 함수 실행
# def my_function():
#     print("Function is executed!")

# # 테스트
# my_function()
# my_function()
# my_function()
