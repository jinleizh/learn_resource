/**
 * @author ctrlzhang on 2016/8/23
 */
public class Test {
    public static void main(String[] args) {

        ThreadPool t = ThreadPool.getThreadPool(10);

        class Task implements Runnable {
            private int idx;

            public Task(int idx) {
                this.idx = idx;
            }

            @Override
            public void run() {
                System.out.println(idx + " do task ...");
            }
        }

        t.execute(new Task(1));
        t.execute(new Task(2));
        t.execute(new Task(3));

        t.destroy();
    }
}
