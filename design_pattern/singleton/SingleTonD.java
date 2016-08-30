/**
 * 优点: 利用静态内部类, lazy loading, 无锁
 *
 * @author ctrlzhang on 2016/8/30
 */
public class SingleTonD {
    private static class SingleTonHolder {
        private static final SingleTonD instance = new SingleTonD();
    }

    private SingleTonD() {}

    public static SingleTonD getInstance() {
        return SingleTonHolder.instance;
    }
}
