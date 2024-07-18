#ifndef ISLEM_IZLEYICI_H
#define ISLEM_IZLEYICI_H

#include <QObject>
#include <QThread>
#include <QString>
#include <QTimer>

class IslemIzleyici : public QObject {
    Q_OBJECT

public:
    explicit IslemIzleyici(QObject *ebeveyn = nullptr);
    void izlemeyiBaslat(const QString &islem);
    void izlemeyiDurdur();

signals:
    void logGuncellendi(const QString &log);

private slots:
    void islemIzle();

private:
    QThread izlemeThread;
    QString izlenenIslem;
    QTimer izlemeZamani;
};

#endif // ISLEM_IZLEYICI_H

