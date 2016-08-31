import java.util.LinkedList;
import java.util.List;

/**
 * 线程池
 *
 * @author ctrlzhang on 2016/8/31
 */
public class ThreadPool {
    /**
     * 工作线程数
     */
    private static int workThreadNum = 5;

    /**
     * 工作线程数组
     */
    private WorkThread[] workThreads;

    /**
     * 线程池对象, 线程安全, lazy loading
     */
    private static volatile ThreadPool threadPool;

    /**
     * 任务队列
     */
    private List<Runnable> taskQueue = new LinkedList<>();

    /**
     * 初始化线程池
     */
    private ThreadPool(int workThreadNum) {
        ThreadPool.workThreadNum = workThreadNum;
        workThreads = new WorkThread[workThreadNum];
        for(int i = 0; i < workThreadNum; i++) {
            workThreads[i] = new WorkThread();
            System.out.println(i + " thread start....");
            workThreads[i].start();
        }
    }

    /**
     * 单例模式-获取线程池
     */
    public static ThreadPool getThreadPool(int workThreadNum) {
        if(null == threadPool) {
            synchronized (ThreadPool.class) {
                if(null == threadPool) {
                    threadPool = new ThreadPool(workThreadNum);
                }
            }
        }

        return threadPool;
    }

    /**
     * 执行任务
     */
    public void execute(Runnable task) {
        synchronized (taskQueue) {
            taskQueue.add(task);
            taskQueue.notify();
        }
    }

    /**
     * 批量执行任务
     */
    public void execute(List<Runnable> tasks) {
        synchronized (taskQueue) {
            for(Runnable r : tasks) {
                taskQueue.add(r);
            }

            taskQueue.notify();
        }
    }

    /**
     * 销毁线程池
     */
    public void destroy() {
        while(!taskQueue.isEmpty()) {
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for(int i = 0; i < ThreadPool.workThreadNum; i++) {
            workThreads[i].stopWork();
            workThreads[i] = null;
        }

        threadPool = null;
        taskQueue.clear();
    }

    /**
     * 获取线程数
     */
    public int getThreadNum() {
        return workThreadNum;
    }

    /**
     * 等待执行的任务数
     */
    public int getWaitedTask() {
        return taskQueue.size();
    }

    class WorkThread extends Thread {
        /**
         * 运行状态
         */
        private boolean isRunning = true;

        /**
         * 停止线程
         */
        public void stopWork() {
            isRunning = false;
            System.out.println("stop work....");
        }

        /**
         * 线程执行--若队列为空，则wait
         */
        @Override
        public void run() {
            Runnable r = null;
            while(isRunning) {
                synchronized (taskQueue) {
                    while(isRunning && taskQueue.isEmpty()) {
                        try {
                            taskQueue.wait(500);
                            System.out.println(" waiting...");
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }

                    if(!taskQueue.isEmpty()) {
                        r = taskQueue.remove(0);
                    }
                }

                if(null != r) {
                    System.out.println("working...");
                    r.run();
                }

                r = null;
            }

            System.out.println("really stop working ...");
        }
    }
}
