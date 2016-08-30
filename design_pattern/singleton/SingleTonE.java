/**
 * 优点:lazy loading
 *     效率高
 *     线程安全
 * 缺点:
 *
 * @author ctrlzhang on 2016/8/30
 */
public class SingleTonE {
    private static volatile SingleTonE instance;

    private SingleTonE() {}

    public static SingleTonE getInstance() {
        if(null == instance) {
            synchronized (SingleTonE.class) {
                if(null == instance) {
                    instance = new SingleTonE();
                }
            }
        }

        return instance;
    }
}
