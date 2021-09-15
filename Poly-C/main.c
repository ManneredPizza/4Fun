#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct term {
    int coeff;
    char var[4];
    int pot[4];
};

void init(struct term *term) {
    //inizializzo tutte le potenze a zero ler la lettura successiva
    for(int j=0; j<4; j++) {
        term->pot[j] = 0;
    }

    //inizializzo tutte le var a x,y,z,w
    term->var[0] = 'x';
    term->var[1] = 'y';
    term->var[2] = 'z';
    term->var[3] = 'w';

    return;
}

struct term read_term() {
    struct term term;
    char c;
    int d;

    scanf("%d", &(term.coeff));

    if(term.coeff == 0) {
        return term;
    }

    init(&term);

    do {
        scanf("%c", &c);
        switch (c) {
            case 'x':
                scanf("%d", &d);
                term.pot[0] += d;
                break;
            case 'y':
                scanf("%d", &d);
                term.pot[1] += d;
                break;
            case 'z':
                scanf("%d", &d);
                term.pot[2] += d;
                break;
            case 'w':
                scanf("%d", &d);
                term.pot[3] += d;
                break;
            default:
                break;
        }
    }
    while(c != '.');

    return term;
}

void write_term(struct term term) {
    if(term.coeff == 0) {
        return;
    }

    //verifica della presenza di un coeff non null
    int coeff_non_nullo = 0;
    for(int i = 0; i<4; i++) {
        if(term.pot[i] != 0) {
            coeff_non_nullo = 1;
        }
    }

    if(abs(term.coeff) != 1 || coeff_non_nullo == 0) {
        printf("%d", term.coeff);
    }

    if(term.coeff == -1) {
        printf("-");
    }

    for(int i = 0; i<4; i++) {
        if(term.pot[i] == 0) {
            continue;
        }

        printf("%c", term.var[i]);
        if(term.pot[i] != 1) {
            printf("%d", term.pot[i]);
        }
    }

    return;
}

int read_poly(struct term *poly) {
    int N;

    scanf("%d", &N);

    for(int i=0; i<N; i++) {
        poly[i] = read_term();
    }

    return N;
}

void write_poly(int n, struct term *poly) {
    if(n == 0) {
        printf("0");
    }
    else {
        for(int i = 0; i<n; i++) {
            if(i != 0 && poly[i].coeff > 0) {
                printf("+");
            }
            write_term(poly[i]);
        }
    }
}

int term_like(struct term term1, struct term term2) {
    int r = 1;

    for(int i = 0; i< 4; i++) {
        if(term1.pot[i] != term2.pot[i]) {
            r = 0;
            break;
        }
    }

    return  r;
}

void del_term(int pos, int n, struct term *poly) {
    for(int i = pos; i<n-1; i++) {
        poly[i] = poly[i+1];
    }

    return;
}

int simplify_poly(int size, struct term *poly) {
    //eliminazione dei termini con coeff nullo
    for(int i=0; i<size; i++) {
        if(poly[i].coeff == 0) {
            del_term(i, size, poly);
            size--;
        }
    }

    //prende un elemento alla volta e lo confornta con i successivi, in caso positivo somma i coeff e elimina il secondo
    for(int i=0; i<size-1; i++) {
        for(int j=i+1; j<size; j++) {
            if(term_like(poly[i], poly[j])) {
                poly[i].coeff += poly[j].coeff;
                del_term(j, size, poly);
                size--;
            }
        }
    } 

    return size;
}

int sum_poly(int n1, struct term *poly1, int n2, struct term *poly2, struct term *poly3) {
    for(int i=0; i<n1; i++) {
        poly3[i] =  poly1[i];
    }
    for(int i=0; i<n2; i++) {
        poly3[n1+i] = poly2[i];
    }

    int n = simplify_poly(n1+n2, poly3);

    return n;
}

struct term mult_term(struct term term1, struct term term2) {
    struct term fin;

    init(&fin);

    fin.coeff = term1.coeff * term2.coeff;

    for(int i = 0; i<4; i++) {
        fin.pot[i] = term1.pot[i] + term2.pot[i];
    }

    return fin;
}

int mult_poly(int n1, struct term *poly1, int n2, struct term *poly2, struct term *poly3) {
    int k = 0;
    
    for(int i = 0; i<n1; i++) {
        for(int j = 0; j<n2; j++) {
            poly3[k] = mult_term(poly1[i], poly2[j]);
            k++;
        }
    }

    int n = simplify_poly(k, poly3);

    return n;
}

int main() {
    char sc;
    struct term term;
    struct term poly1[1024], poly2[1024], poly3[2048];
    int n1, n2, n;

    do {
        scanf("%c", &sc);

        switch(sc) {
            case 'T':
                term = read_term();
                write_term(term);
                break;
            case 'S':
                n = read_poly(poly1);
                n = simplify_poly(n, poly1);
                write_poly(n, poly1);
                break;
            case '+':
                n1 = read_poly(poly1);
                n2 = read_poly(poly2);

                n1 = simplify_poly(n1, poly1);
                n2 = simplify_poly(n2, poly2);
                
                n = sum_poly(n1, poly1, n2, poly2, poly3);
                write_poly(n, poly3);
                break;
            case '*':
                n1 = read_poly(poly1);
                n2 = read_poly(poly2);

                n1 = simplify_poly(n1, poly1);
                n2 = simplify_poly(n2, poly2);

                n = mult_poly(n1, poly1, n2, poly2, poly3);
                write_poly(n, poly3);
                break;
            default:
                break;
        }
    }
    while(sc != '.');

    return 0;
}