import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('5주차 과제/math01_lab/data/class_score_kr.csv')
    class_en = read_data('5주차 과제/math01_lab/data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [(40/125)*midterm + (60/100)*final for (midterm, final) in class_kr]

    midterm_en, final_en = zip(*class_en)
    total_en = [(40/125)*midterm + (60/100)*final for (midterm, final) in class_en]

    # midterm_en, final_en = [0, 0] 
    # total_en = [0]

    # TODO) Plot midterm/final scores as points

    # TODO) Plot total scores as a histogram

    # Plot midterm and final scores as scatter plots
    plt.figure(figsize=(7, 10))

    plt.subplot(2, 1, 1)
    plt.scatter(midterm_kr, final_kr, color='red', label='Korean', marker='o')
    plt.scatter(midterm_en, final_en, color='blue', label='English', marker='+')
    plt.title('Midterm vs Final Scores')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.hist(total_kr, bins=10, alpha=0.7, color='red', label='Korean')
    plt.hist(total_en, bins=10, alpha=0.4, color='blue', label='English')
    plt.title('Total Score Distribution')
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.legend()

    plt.tight_layout()
    plt.show()