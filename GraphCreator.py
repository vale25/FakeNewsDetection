from pylab import *

def createGraph(lista,lista2,lista3,lista4,lista5,lista6,lista7,lista8,lista9,lista10, lenght, value):

    t = arange(0.0, lenght, 1)
    s = lista
    s2 = lista2
    s3 = lista3
    s4 = lista4
    s5 = lista5
    s6 = lista6
    s7 = lista7
    s8 = lista8
    s9 = lista9
    s10 = lista10
    axis([0.0, 3100.0, 0.0, 1.1])
    plot(t, s, label='news1')
    plot(t, s2, label='news2')
    plot(t, s3, label='news3')
    plot(t, s4, label='news4')
    plot(t, s5, label='news5')
    plot(t, s6, label='news6')
    plot(t, s7, label='news7')
    plot(t, s8, label='news8')
    plot(t, s9, label='news9')
    plot(t, s10, label='news10')
    plt.legend()

    if value == 0:
        xlabel("News")
        ylabel("Cosine Similarity")
        title("Syntactic similarity of fake news with the FakeNews dataset")
    if value == 1:
        xlabel("News")
        ylabel("Cosine Similarity")
        title("Syntactic similarity of real news with the RealNews dataset")
    if value == 2:
        xlabel("News")
        ylabel("Cosine Similarity")
        title("Syntactic similarity of fake news with the RealNews dataset")
    if value == 3:
        xlabel("News")
        ylabel("Cosine Similarity")
        title("Syntactic similarity of real news with the FakeNews dataset")
    if value == 4:
        xlabel("News")
        ylabel("Semantic Similarity")
        title("Semantic similarity of fake news with the FakeNews dataset")
    if value == 5:
        xlabel("News")
        ylabel("Semantic Similarity")
        title("Semantic similarity of real news with the RealNews dataset")
    if value == 6:
        xlabel("News")
        ylabel("Semantic Similarity")
        title("Semantic similarity of fake news with the RealNews dataset")
    if value == 7:
        xlabel("News")
        ylabel("Semantic Similarity")
        title("Semantic similarity of real news with the FakeNews dataset")


    grid(True)
    show()