/**
 * 优点: 利用静态内部类, lazy loading, 无锁
 *       SingletonHolder类只有被主动使用时，才会实例化
 *       即，调用getInstance方法时，才会调用new SingleTonD
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
