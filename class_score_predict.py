import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('6주차 과제/math02_lab/data/class_score_kr.csv', delimiter=',')
    class_en = np.loadtxt('6주차 과제/math02_lab/data/class_score_en.csv', delimiter=',')
    data = np.vstack((class_kr, class_en))

    # Estimate a line, final = slope * midterm + y_intercept
    #line = [0, 0] # TODO) Please find the best [slope, y_intercept] from 'data'
    # Extract midterm and final scores
    midterms = data[:, 0]
    finals = data[:, 1]
    
    N = len(midterms)

    sum_x = np.sum(midterms)
    sum_y = np.sum(finals)
    sum_x_squared = np.sum(midterms ** 2)
    sum_xy = np.sum(midterms * finals)

    slope = (N * sum_xy - sum_x * sum_y) / (N * sum_x_squared - sum_x ** 2)
    y_intercept = (sum_y - slope * sum_x) / N

    line = [slope, y_intercept] 

    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        try:
            given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
            if given == '' or float(given) < 0:
                break
            print(f'A) Your final score is expected to {final(float(given)):.3f}.')
        except Exception as ex:
            print(f'Cannot answer the question. (message: {ex})')
            break

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()
