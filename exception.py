import sys
def get_error_detail_massage(error_masg:str, error_detail_from_run_time:sys)-> str:
    """
    this function is for getting formatted error massage

    """
    _,_,exc_tb = error_detail_from_run_time.exc_info()
    line_number = exc_tb.tb_lineno
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_massage = f"Error occured in python script: [{file_name}] at line number: [{line_number}]  massage: [{error_masg}]"
    return error_massage

class CustomException(Exception):
    def __init__(self,error_massage_from_exception: str, error_detail_from_run_time:sys):
        super().__init__(error_massage_from_exception)
        self.error_detail = get_error_detail_massage(error_masg = error_massage_from_exception
                                                     ,error_detail_from_run_time=error_detail_from_run_time)
    def __str__(self):
        return self.error_detail
    
if __name__ == '__main__':
    try:
        raise Exception("this is a test exception")
    except Exception as e:
        raise CustomException(e, sys)