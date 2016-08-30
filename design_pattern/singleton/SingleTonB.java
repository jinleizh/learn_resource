/**
 * 优点: lazy loading
 * 缺点: 线程不安全
 *
 * @author ctrlzhang on 2016/8/30
 */
public class SingleTonB {
    private volatile static SingleTonB instance; //volatile保证变量对多线程可见
    private SingleTonB() {}

    public static SingleTonB getInstance() {
        if(null == instance) {
            instance = new SingleTonB();
        }

        return instance;
    }
}
