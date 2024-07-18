#ifndef ANA_PENCERE_H
#define ANA_PENCERE_H

#include <QMainWindow>
#include <QLabel>
#include <QComboBox>
#include <QPushButton>
#include <QTextEdit>
#include <QLineEdit>
#include "islem_izleyici.h"

class AnaPencere : public QMainWindow {
    Q_OBJECT

public:
    AnaPencere(QWidget *ebeveyn = nullptr);
    ~AnaPencere();

private slots:
    void izleBaslat();
    void izleDurdur();
    void logKaydet();
    void islemleriYukle();
    void logFiltrele();
    void logAra();

private:
    QLabel *logoEtiketi;
    QComboBox *islemComboBox;
    QPushButton *baslatDugmesi;
    QPushButton *durdurDugmesi;
    QPushButton *kaydetDugmesi;
    QPushButton *filtreleDugmesi;
    QPushButton *araDugmesi;
    QTextEdit *logMetinEdit;
    QLineEdit *filtreGirdi;
    QLineEdit *araGirdi;
    IslemIzleyici *islemIzleyici;
    QString logVeri;
};

#endif // ANA_PENCERE_H

