/**
 * @author ctrlzhang on 2016/8/23
 */
public class Test {
    public static void main(String[] args) {
        System.out.println("good");
        SingleTonA test = SingleTonA.getInstance();
        System.out.println(test.toString());

        SingleTonB testB = SingleTonB.getInstance();
        System.out.println(testB.toString());

        SingleTonD singleTonD = SingleTonD.getInstance();
        System.out.println(singleTonD.toString());

        SingleTonF singleTonF = SingleTonF.INSTANCE;
        System.out.println(singleTonF.toString());
        singleTonF.test();

        SingleTonE singleTonE = SingleTonE.getInstance();
        System.out.println(singleTonE.toString());
    }
}
