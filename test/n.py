import multiprocessing
import time

# 具体的处理函数，负责处理单个任务
def func(msg):
  # for i in range(3):
    print (msg)
    time.sleep(1)
    return "done " + msg
if __name__ == "__main__":
    # 进程池，创建多个进程，并行执行
    pool = multiprocessing.Pool(processes=4)
    # 把运行的结果添加到一个列表里，关注每个进程的执行结果
    result = []
    # 生产msg，并加入进程池
    for i in range(10):
        msg = "hello %d" %(i)
        # apply_async 它是非阻塞且支持结果返回进行回调
        result.append(pool.apply_async(func, (msg, )))
        # 关闭进程池，使其不在接受新的任务
    pool.close()
    # 主进程阻塞等待子进程的退出，join方法必须在close或terminate之后使用。
    pool.join()
    # 查看执行结果
    for res in result:
        print (res.get())
    print ("Sub-process(es) done.")