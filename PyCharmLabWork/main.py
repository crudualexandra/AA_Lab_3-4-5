import lab3.analysis_lab3 as lab3
import lab4.analysis_lab4 as lab4
import lab5.analysis_lab5 as lab5

if __name__=='__main__':
    print('Lab3…'); lab3.analyze()
    print('Lab4…'); lab4.analyze([50,100,200,400],p_sparse=0.01,p_dense=0.7)
    print('Lab5…'); lab5.analyze([50,100,200,400],p_sparse=0.01,p_dense=0.7)
    print('Done.')
