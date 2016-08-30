/**
 * 优点: lazy loading
 *      线程安全
 * 缺点: 锁效率低, 每次都要加锁，实际上只有在初始阶段, 锁才有意义, 初始化之后锁反而拖慢了速度.
 * @author ctrlzhang on 2016/8/30
 */
public class SingleTonC {
    private volatile static SingleTonC singleTonC;

    private SingleTonC() {

    }

    public static synchronized SingleTonC getInstance() {
        if(null == singleTonC) {
            singleTonC = new SingleTonC();
        }

        return singleTonC;
    }
}
