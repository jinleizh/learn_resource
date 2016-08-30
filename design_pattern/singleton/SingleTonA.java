/**
 * 缺点:没有lazy loading
 * 优点:线程安全
 *     利用了classloader机制,保证了只有一个线程进行类的初始化.
 *
 * @author ctrlzhang on 2016/8/30
 */
public class SingleTonA {
    private static final SingleTonA mSingleTon = new SingleTonA();

    private SingleTonA() {

    }

    public static SingleTonA getInstance() {
        return mSingleTon;
    }
}
